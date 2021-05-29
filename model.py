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
        self.ws3 = nn.Linear((config['hidden_dim']*2), (config['hidden_dim']*2))
        self.ws4 = nn.Linear((config['hidden_dim']*2), 1)
        self.softmax = nn.Softmax(dim=1)
        self.discourse_encoder = nn.LSTM(config['hidden_dim']*2, config['hidden_dim'], config['num_layers'],
                              batch_first=True, bidirectional=config['bidirectional'])

    def init_weights(self):
        for name, param in self.discourse_encoder.state_dict().items():
            if 'weight' in name: nn.init.xavier_normal(param)

        nn.init.xavier_uniform(self.ws3.state_dict()['weight'])
        self.ws3.bias.data.fill_(0)
        nn.init.xavier_uniform(self.ws4.state_dict()['weight'])
        self.ws4.bias.data.fill_(0)

    def forward(self, sent_encoding, hidden_ctxt=None):
        inner_pred = self.drop(sent_encoding)
        inner_pred, hidden_op = self.discourse_encoder.forward(inner_pred[None, :, :])
        self_attention = F.tanh(self.ws3(self.drop(inner_pred)))
        self_attention = self.ws4(self.drop(self_attention)).squeeze(2)
        doc_self_attention = self.softmax(self_attention)
        doc_inner_pred = inner_pred.squeeze()
        doc_disc_encoding = torch.sum(doc_inner_pred * doc_self_attention.unsqueeze(-1), dim=1)
        return inner_pred, doc_disc_encoding


#  Returns Transition scores, note it ignores headline and the first sentence
#  Output size Number of sentences-1 * 2, start from the second sentence
# class ParentTree(nn.Module):
#
#     def __init__(self, config):
#         super(ParentTree, self).__init__()
#         self.W1 = nn.Linear(config['hidden_dim']*4, config['hidden_dim']*2, bias=False)
#         self.W2 = nn.Linear(config['hidden_dim']*2, config['hidden_dim']*2, bias=False)
#         self.vt = nn.Linear(config['hidden_dim']*2, 1)
#         self.softmax = nn.Softmax(dim=1)
#         self.drop = nn.Dropout(config['dropout'])
#
#     def init_weights(self):
#         nn.init.xavier_uniform(self.W1.state_dict()['weight'])
#         nn.init.xavier_uniform(self.W2.state_dict()['weight'])
#         nn.init.xavier_uniform(self.vt.state_dict()['weight'])
#         self.vt.bias.data.fill_(0)
#
#     def attentions(self, e1, e2, mask):
#         # e1 = self.W1(self.drop(encoder_outputs.squeeze()))
#         # e2 = self.W2(self.drop(decoder_step))
#         e2 = e2.squeeze()
#         # print((e1-e2).size(), (e1*e2).size())
#         enc = self.W2(self.drop(torch.tanh(self.W1(torch.cat([e1*e2, e1-e2],1)))))
#         attn = self.vt(self.drop(torch.tanh(enc))) + -10000. * (mask == 0).float()
#         return attn.squeeze()
#
#     def get_sample(self, attn, is_test):
#         scores = F.softmax(attn)
#         if is_test:
#             _, predicts = torch.max(scores, 0)
#         else:
#             predicts = Categorical(scores).sample()
#         return predicts.item()
#
#     def forward(self, sent_encodings, hidden_embedding, is_test):
#         sent_to_parent = [0, 0]
#         rl_loss = None
#         sent_encodings = sent_encodings.transpose(0,1)
#         maxlen = sent_encodings.size(0) # No of sentences, ROOT
#         for ind in range(2, maxlen, 1):  # Ignore ROOT and the first sentence, obvious parents
#             mask = [[0] for _ in range(maxlen)]
#             for i in range(ind): # index and sentence numbers are aligned, so +1
#                 mask[i][0] = 1
#             mask = torch.LongTensor(mask).cuda()
#             scores = self.attentions(sent_encodings[ind], sent_encodings, mask)
#             parent = self.get_sample(scores, is_test)
#             if not rl_loss:
#                 rl_loss = F.cross_entropy(scores[:ind].view(1, -1), torch.LongTensor([parent]).cuda())
#             else:
#                 rl_loss += F.cross_entropy(scores[:ind].view(1, -1), torch.LongTensor([parent]).cuda())
#             sent_to_parent.append(parent)  # first headline, so index and sentence numbers are aligned
#
#         return sent_to_parent, rl_loss/(maxlen-2+1e-5) if rl_loss else 0


# """
# Based on pointer network
# Uncomment this and comment out the above ParentTree code
class ParentTree(nn.Module):

    def __init__(self, config):
        super(ParentTree, self).__init__()
        self.W1 = nn.Linear(config['hidden_dim']*2, config['hidden_dim']*2, bias=False)
        self.W2 = nn.Linear(config['hidden_dim']*2, config['hidden_dim']*2, bias=False)
        self.vt = nn.Linear(config['hidden_dim']*4, 1)
        self.decoding_rnn = nn.LSTMCell(input_size=config['hidden_dim']*2, hidden_size=config['hidden_dim']*2)
        self.softmax = nn.Softmax(dim=1)
        self.drop = nn.Dropout(config['dropout'])

    def init_weights(self):
        nn.init.xavier_uniform(self.W1.state_dict()['weight'])
        nn.init.xavier_uniform(self.W2.state_dict()['weight'])
        nn.init.xavier_uniform(self.vt.state_dict()['weight'])
        for name, param in self.decoding_rnn.state_dict().items():
            if 'weight' in name: nn.init.xavier_normal(param)
        self.vt.bias.data.fill_(0)

    def attentions(self, decoder_step, encoder_outputs, mask):
        e1 = self.W1(self.drop(encoder_outputs.squeeze()))
        e2 = self.W2(self.drop(decoder_step))
        enc = torch.cat([e1*e2, e1-e2],1)
        attn = self.vt(self.drop(torch.tanh(enc))) + -10000. * (mask == 0).float()
        return attn.squeeze()

    def get_sample(self, attn, is_test):
        scores = F.softmax(attn)
        if is_test:
            _, predicts = torch.max(scores, 0)
        else:
            predicts = Categorical(scores).sample()
        return predicts.item()

    def forward(self, sent_encodings, hidden_embedding, is_test):
        sent_to_parent = [0, 0]
        rl_loss = None
        sent_encodings = sent_encodings.transpose(0,1)
        maxlen = sent_encodings.size(0) # No of sentences, ROOT
        decoder_hidden = hidden_embedding
        for ind in range(2, maxlen, 1):  # Ignore ROOT and the first sentence, obvious parents
            mask = [[0] for _ in range(maxlen)]
            for i in range(ind): # index and sentence numbers are aligned, so +1
                mask[i][0] = 1
            mask = torch.LongTensor(mask).cuda()
            decoder_input = sent_encodings[ind]
            h_i, c_i = self.decoding_rnn(decoder_input, decoder_hidden)
            decoder_hidden = (h_i, c_i)
            scores = self.attentions(h_i, sent_encodings, mask)
            parent = self.get_sample(scores, is_test)
            if not rl_loss:
                rl_loss = F.cross_entropy(scores[:ind].view(1, -1), torch.LongTensor([parent]).cuda())
            else:
                rl_loss += F.cross_entropy(scores[:ind].view(1, -1), torch.LongTensor([parent]).cuda())
            sent_to_parent.append(parent)  # first headline, so index and sentence numbers are aligned

        return sent_to_parent, rl_loss/(maxlen-2+1e-5) if rl_loss else 0
# """


class DiscourseAct(nn.Module):

    def __init__(self, config):
        super(DiscourseAct, self).__init__()
        self.pre_pred = nn.Linear((config['hidden_dim']*2*2), config['hidden_dim']*2)
        self.pred = nn.Linear((config['hidden_dim']*2), config['out_dim'])
        self.drop = nn.Dropout(config['dropout'])
        self.softmax = nn.Softmax(dim=1)

    def init_weights(self):
        nn.init.xavier_uniform(self.pre_pred.state_dict()['weight'])
        self.pre_pred.bias.data.fill_(0)
        nn.init.xavier_uniform(self.pred.state_dict()['weight'])
        self.pred.bias.data.fill_(0)

    def get_du_representations(self, sent_encoding, parents):
        out_1 = []
        sent_encoding = sent_encoding.squeeze(0)
        seq_len = sent_encoding.size(0)

        for i in range(1, seq_len, 1):
            out_1.append(torch.cat([sent_encoding[i].view(1,-1), sent_encoding[parents[i]].view(1,-1)], 1))

        return torch.cat(out_1, 0)

    def forward(self, sent_encoding, parents):
        out = self.get_du_representations(sent_encoding, parents)
        pre_pred = F.tanh(self.pre_pred(self.drop(out)))
        return self.pred(self.drop(pre_pred))


class Classifier(nn.Module):

    def __init__(self, config):
        super(Classifier, self).__init__()
        self.sentence_encoder = SentenceEncoder(config)
        self.discourse_encoder = DiscourseEncoder(config)
        self.discourse_act = DiscourseAct(config)
        self.parent_tree = ParentTree(config)

    def init_weights(self):
        self.sentence_encoder.init_weights()
        self.discourse_encoder.init_weights()
        self.discourse_act.init_weights()
        self.parent_tree.init_weights()

    def get_tree(self, sent_encoding, hidden_embedding, is_test):
        return self.parent_tree.forward(sent_encoding, hidden_embedding, is_test)

    def get_rule_transition_scores(self, sent_encoding, hidden_embedding, rule_based_trans_sents):
        return self.topic_segmenter.rule_based_scores(sent_encoding, hidden_embedding, rule_based_trans_sents)

    def get_sentence_encoding(self, outp_ctxt, ctxt_mask, length, hidden_ctxt=None):
        return self.sentence_encoder.forward(outp_ctxt, ctxt_mask, length, hidden_ctxt)

    def get_discourse_encoding(self, sent_encoding):
        return self.discourse_encoder.forward(sent_encoding)

    def get_discourse_tags(self, sent_encoding, parent_sents):
        return self.discourse_act.forward(sent_encoding, parent_sents)

    def forward(self, sentence, length, is_test=False, hidden_ctxt=None):
        outp_ctxt, ctxt_mask = get_word_embeddings(sentence)
        sent_encoding = self.get_sentence_encoding(outp_ctxt, ctxt_mask, length)
        sent_encoding, doc_encoding = self.get_discourse_encoding(sent_encoding)
        hidden_op = (doc_encoding.view(1,-1), doc_encoding.view(1,-1))
        parent_sents, rl_loss = self.get_tree(sent_encoding, hidden_op, is_test)
        # if is_test:
        #     print(parent_sents)
        pred = self.get_discourse_tags(sent_encoding, parent_sents)

        critic_parent_sents, _ = self.get_tree(sent_encoding, hidden_op, True)
        critic_pred = self.get_discourse_tags(sent_encoding, critic_parent_sents)

        return pred, critic_pred, rl_loss
