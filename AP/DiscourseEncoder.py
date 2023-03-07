import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence, pad_sequence
import numpy as np
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
import transformers


import warnings
warnings.filterwarnings('ignore')


class Embedding(nn.Module):
    def __init__(self, config):
        super(Embedding, self).__init__()
        
        self.device = config['device']

        self.roberta = AutoModel.from_pretrained(config['model_type']) #swap roberta name with emn_model
        # print("config['model_type'] ", config['model_type'])
        self.roberta = self.roberta.to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(config['model_type'], padding = True, max_length = 100) 
        # print("tokenizer.is_fast ", self.tokenizer.is_fast)
        self.sum_hidden_states = config["sum_hidden_states"] #if true, sums the token representations of last 4 hidden states. otherwise uses final hidden state only
        self.nfinetune = config['nfinetune']

        for param in self.roberta.parameters():
            param.requires_grad = False

        n_layers = 12
        if self.nfinetune > 0:
            for param in self.roberta.pooler.parameters():
                param.requires_grad = True
            for i in range(n_layers-1, n_layers-1-self.nfinetune, -1):
                print("Putting layer {} to fine-tune".format(i))
                for param in self.roberta.encoder.layer[i].parameters():
                    param.requires_grad = True
        else: self.roberta.eval()

    #either sum last 4 hidden layers or use last hidden state or CLS reps
    def get_word_embeddings(self, sentence_batch):
        #sentence_batch: gets a list of strings, where each string is an utterance

        batch_encoded = self.tokenizer(sentence_batch, padding=True, truncation=True, return_tensors="pt").to(self.device)
        attention_mask = batch_encoded.attention_mask
        out = self.roberta(**batch_encoded, output_hidden_states = self.sum_hidden_states)
        if self.sum_hidden_states == False: return out.last_hidden_state, attention_mask
                                        #last_hidden_state: (batch size, max token, 768)

        #sum last 4 hidden states
        embeddings = torch.stack(out.hidden_states, dim=0) #stack all layer outputs
        embeddings = embeddings.permute(1,2,0,3) #batch, tokens, layers, dim
        emb = embeddings[:,:,-4:,:].sum(dim = 2) #(batch, max tokens, dim)
        return emb, attention_mask


class DiscourseEncoder(nn.Module):

    def __init__(self, inp_dim, hid_dim, drop):
        super(DiscourseEncoder, self).__init__()
        self.input_size = inp_dim
        self.hidden_dim = hid_dim
        print("self.input_size ", self.input_size)
        print("self.hidden_dim ", self.hidden_dim)

        self.rnn = nn.LSTM(self.input_size, self.hidden_dim, dropout=drop,
                               bidirectional=True, num_layers=1, batch_first=True)

    def forward(self, text_len_tensor, text_tensor):
        packed = pack_padded_sequence(
            text_tensor,
            text_len_tensor,
            batch_first=True,
            enforce_sorted=False
        )
        rnn_out, (_, _) = self.rnn(packed, None)
        rnn_out, _ = pad_packed_sequence(rnn_out, batch_first=True)

        return rnn_out


class SentenceEncoder(nn.Module):
    def __init__(self, config):
        super(SentenceEncoder, self).__init__()
        self.context_encoder = nn.LSTM(config['embedding_dim'], config['hidden_dim'], config['num_layers'],
                              batch_first=True, bidirectional=config['bidirectional']) #, dropout=config['dropout']
        self.inner_pred = nn.Linear((config['hidden_dim']*2), config['hidden_dim']*2)
        self.ws1 = nn.Linear((config['hidden_dim']*2), (config['hidden_dim']*2))
        self.ws2 = nn.Linear((config['hidden_dim']*2), 1)
        self.softmax = nn.Softmax(dim=1)
        self.drop = nn.Dropout(config['dropout'])

    def init_weights(self):
        for name, param in self.context_encoder.state_dict().items():
            if 'weight' in name: nn.init.xavier_normal(param)
        nn.init.xavier_uniform(self.ws1.state_dict()['weight'])
        self.ws1.bias.data.fill_(0)
        nn.init.xavier_uniform(self.ws2.state_dict()['weight'])
        self.ws2.bias.data.fill_(0)
        nn.init.xavier_uniform(self.inner_pred.state_dict()['weight'])
        self.inner_pred.bias.data.fill_(0)

    def forward(self, outp_ctxt, ctxt_mask, length, hidden_ctxt=None):
        outp, _ = self.context_encoder.forward(outp_ctxt, hidden_ctxt)
        self_attention = F.tanh(self.ws1(self.drop(outp)))
        self_attention = self.ws2(self.drop(self_attention)).squeeze()
        self_attention = self_attention + -10000*(ctxt_mask == 0).float()
        self_attention = self.drop(self.softmax(self_attention))
        sent_encoding = torch.sum(outp*self_attention.unsqueeze(-1), dim=1)

        return F.tanh(self.inner_pred(self.drop(sent_encoding)))


class Encoder(nn.Module):
    def __init__(self, config):#, args):
        super(Encoder, self).__init__()

        # self.args = args
        self.use_CLS = config['use_CLS']
        self.embedding = Embedding(config['embedding_config'])
        if not config['use_CLS']: self.sentence_encoder = SentenceEncoder(config)
        inp_dim = config['hidden_dim'] * 2 if config['bidirectional'] else config['hidden_dim']
        if config['use_CLS']: inp_dim = 768
        self.discourse_encoder = DiscourseEncoder(inp_dim, int(config['hidden_dim']/2), config['dropout'])
        self.drop = nn.Dropout(config['dropout'])


    def flatten_samples(self, examples_set):
        flat_list = []

        for class_list in examples_set:
            for samples in class_list:
                for s in samples:
                    flat_list.append(s)

        return flat_list
        

    def forward(self, data):
        utterance_embs = []
        sentences = data['text_raw'] #list of sentences

        for sentence in sentences:
            outp_emb, attention_mask = self.embedding.get_word_embeddings(sentence)
            #outp_emb (#sents, max tokens in any, 768)
            if self.use_CLS: sent_encoding = outp_emb[:, 0] #get [cls] token emb from last layer

            else: sent_encoding = self.sentence_encoder.forward(outp_emb, attention_mask) # #utts, 400
            utterance_embs.append(sent_encoding) #sent_encoding: (bs, hid*2) or (bs, 768)

        utterance_embs = pad_sequence(utterance_embs, batch_first=True) #bs, max_len, 768


        utterance_embs = self.discourse_encoder(data["text_len_tensor"].cpu(), utterance_embs) # [batch_size, mx_len, D_g]
        return self.drop(utterance_embs)
