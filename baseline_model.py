import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
import numpy as np
import torch.nn.functional as F
from torch.autograd import Variable
from torch.distributions import Categorical
from allennlp.modules.elmo import Elmo, batch_to_ids


CUDA = torch.cuda.is_available()
options_file = "https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x4096_512_2048cnn_2xhighway/elmo_2x4096_512_2048cnn_2xhighway_options.json"
weight_file = "https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x4096_512_2048cnn_2xhighway/elmo_2x4096_512_2048cnn_2xhighway_weights.hdf5"

elmo = Elmo(options_file, weight_file, 1, dropout=0.0, requires_grad=False)
if CUDA:
    elmo = elmo.cuda()


def get_word_embeddings(sentence):
    character_ids = batch_to_ids(sentence)
    if CUDA:
        character_ids = character_ids.cuda()
    embedding = elmo(character_ids)
    outp_ctxt = embedding['elmo_representations'][0]
    ctxt_mask = embedding['mask']
    return outp_ctxt, ctxt_mask


class BiLSTM(nn.Module):

    def __init__(self, config, is_pos=False):
        super(BiLSTM, self).__init__()
        self.bidirectional = config['bidirectional']
        self.num_layers = config['num_layers']
        self.hidden_dim = config['hidden_dim']
        self.embedding_dim = config['embedding_dim']

        self.bilstm = nn.LSTM(self.embedding_dim, self.hidden_dim, config['num_layers'],
                              batch_first=True, bidirectional=config['bidirectional']) #, dropout=config['dropout']

    def init_weights(self):
        for name, param in self.bilstm.state_dict().items():
            if 'weight' in name: nn.init.xavier_normal(param)

    def forward(self, emb, len_inp, hidden=None):
        len_inp = len_inp.cpu().numpy() if CUDA else len_inp.numpy()
        len_inp, idx_sort = np.sort(len_inp)[::-1], np.argsort(-len_inp)
        len_inp = len_inp.copy()
        idx_unsort = np.argsort(idx_sort)

        idx_sort = torch.from_numpy(idx_sort).cuda() if CUDA else torch.from_numpy(idx_sort)
        emb = emb.index_select(0, Variable(idx_sort))

        emb_packed = pack_padded_sequence(emb, len_inp, batch_first=True)
        outp, _ = self.bilstm(emb_packed, hidden)
        outp = pad_packed_sequence(outp, batch_first=True)[0]

        idx_unsort = torch.from_numpy(idx_unsort).cuda() if CUDA else torch.from_numpy(idx_unsort)
        outp = outp.index_select(0, Variable(idx_unsort))
        return outp

    def init_hidden(self, batch_size):
        weight = next(self.parameters()).data
        num_directions = 2 if self.bidirectional else 1
        return (Variable(weight.new(self.num_layers*num_directions, batch_size, self.hidden_dim).zero_()),
                Variable(weight.new(self.num_layers*num_directions, batch_size, self.hidden_dim).zero_()))


#  Returns LSTM based sentence encodin, dim=1024, elements of vector in range [-1,1]
class SentenceEncoder(nn.Module):

    def __init__(self, config):
        super(SentenceEncoder, self).__init__()
        self.context_encoder = BiLSTM(config)
        self.inner_pred = nn.Linear((config['hidden_dim']*2), config['hidden_dim']*2) # Prafulla 3
        self.ws1 = nn.Linear((config['hidden_dim']*2), (config['hidden_dim']*2))
        self.ws2 = nn.Linear((config['hidden_dim']*2), 1)
        self.softmax = nn.Softmax(dim=1)
        self.drop = nn.Dropout(config['dropout'])

    def init_weights(self):
        nn.init.xavier_uniform(self.ws1.state_dict()['weight'])
        self.ws1.bias.data.fill_(0)
        nn.init.xavier_uniform(self.ws2.state_dict()['weight'])
        self.ws2.bias.data.fill_(0)
        nn.init.xavier_uniform(self.inner_pred.state_dict()['weight'])
        self.inner_pred.bias.data.fill_(0)
        self.context_encoder.init_weights()

    def forward(self, outp_ctxt, ctxt_mask, length, hidden_ctxt=None):
        outp = self.context_encoder.forward(outp_ctxt, length, hidden_ctxt)

        self_attention = F.tanh(self.ws1(self.drop(outp)))
        self_attention = self.ws2(self.drop(self_attention)).squeeze()
        self_attention = self_attention + -10000*(ctxt_mask == 0).float()
        self_attention = self.drop(self.softmax(self_attention))
        sent_encoding = torch.sum(outp*self_attention.unsqueeze(-1), dim=1)

        return F.tanh(self.inner_pred(self.drop(sent_encoding)))


class DiscourseEncoder(nn.Module):

    def __init__(self, config):
        super(DiscourseEncoder, self).__init__()
        self.drop = nn.Dropout(config['dropout'])
        self.discourse_encoder = nn.LSTM(config['hidden_dim']*2, config['hidden_dim']*2, config['num_layers'],
                              batch_first=True, bidirectional=False)

    def init_weights(self):
        for name, param in self.discourse_encoder.state_dict().items():
            if 'weight' in name: nn.init.xavier_normal(param)

    def forward(self, sent_encoding, hidden_ctxt=None):
        inner_pred = self.drop(sent_encoding)
        inner_pred, hidden_op = self.discourse_encoder.forward(inner_pred)
        # print(inner_pred.size(), inner_pred[:,-1,:].size())
        return inner_pred[:, -1, :]  # Last hidden state


class Classifier(nn.Module):

    def __init__(self, config):
        super(Classifier, self).__init__()
        self.sentence_encoder = SentenceEncoder(config)
        self.discourse_encoder = DiscourseEncoder(config)
        self.pre_pred = nn.Linear((config['hidden_dim']*2), config['hidden_dim']*2)
        self.pred = nn.Linear((config['hidden_dim']*2), config['out_dim'])
        self.drop = nn.Dropout(config['dropout'])
        self.init_weights()

    def init_weights(self):
        self.sentence_encoder.init_weights()
        self.discourse_encoder.init_weights()
        nn.init.xavier_uniform(self.pre_pred.state_dict()['weight'])
        self.pre_pred.bias.data.fill_(0)
        nn.init.xavier_uniform(self.pred.state_dict()['weight'])
        self.pred.bias.data.fill_(0)

    def forward(self, sentence, length, history_len=5, hidden_ctxt=None):
        outp_ctxt, ctxt_mask = get_word_embeddings(sentence)
        sent_encoding = self.sentence_encoder.forward(outp_ctxt, ctxt_mask, length, hidden_ctxt)
        # modify size
        sent_encoding = sent_encoding.view(-1,history_len,sent_encoding.size(-1))
        sent_encoding = self.discourse_encoder.forward(sent_encoding)
        pre_pred = F.tanh(self.pre_pred(self.drop(sent_encoding)))
        return self.pred(self.drop(pre_pred))