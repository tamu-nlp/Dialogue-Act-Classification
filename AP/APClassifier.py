import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
import numpy as np
import torch.nn.functional as F
from torch.autograd import Variable
from torch.distributions import Categorical
from CRF import CRF
from DiscourseEncoder import Encoder
import warnings
warnings.filterwarnings('ignore')

#3-way part classifier with crf, then takes predicted Bs and connects with most recent potential A -- heuristics linkage
#DA classifier is the baseline classifier
#trained in a multitask setting -- share the base layers but no other information passed to each other.

class JointClassifier(nn.Module):
    def __init__(self, config):
        super(JointClassifier, self).__init__()
        self.device = config['device']
        self.ASIST = config['ASIST']
        self.discourse_encoder = Encoder(config)
        self.CRF = CRF(config['out_dim_part'], self.device)
        if not config['ASIST']:
            self.pre_pred = nn.Linear((config['hidden_dim']), config['hidden_dim'])
            self.pred = nn.Linear((config['hidden_dim']), config['out_dim'])
        self.pre_pred_part = nn.Linear((config['hidden_dim']), config['hidden_dim'])
        self.pred_part = nn.Linear((config['hidden_dim']), config['out_dim_part'])
        self.drop = nn.Dropout(config['dropout'])

    def forward(self, data, get_loss=True):
        batch_size = data['text_len_tensor'].shape[0]

        sent_encoding = self.discourse_encoder(data)
        pre_pred_part = F.tanh(self.pre_pred_part(self.drop(sent_encoding)))
        pred_part = self.pred_part(self.drop(pre_pred_part))

        pred_part_flattened = self.unpad_features(pred_part, data['text_len_tensor'])

        #get best label seq 
               
        all_ap_predictions = []
        ap_loss = 0.0
        for dialogue_ind in range(len(pred_part_flattened)):
            dialogue_part_pred = pred_part_flattened[dialogue_ind]

            score, tag_seq = self.CRF._viterbi_decode(dialogue_part_pred)
            predict = torch.zeros(data['text_len_tensor'][dialogue_ind])
            j = 0
            for i in range(predict.size(0)):
                predict[i] = tag_seq[j]#] = 1
                j += 1
            # return pred, predict #[a 1-D tensor with predicted part ind]
            all_ap_predictions.append(predict)
            if get_loss: 
                true_tags = torch.tensor(data['ap_part_labels'][dialogue_ind]).long().to(self.device)
                assert dialogue_part_pred.shape[0] == true_tags.shape[0]
                loss_crf = self.CRF._get_neg_log_likilihood_loss(dialogue_part_pred, true_tags)
                ap_loss+=loss_crf[0]
        ap_loss = ap_loss/batch_size

        pred = None
        if not self.ASIST: 
            pre_pred = F.tanh(self.pre_pred(self.drop(sent_encoding)))
            pred = self.pred(self.drop(pre_pred))
            pred = self.unpad_features(pred, data['text_len_tensor'])
            pred = torch.cat(pred, dim=0).to(self.device)


        return pred, all_ap_predictions, ap_loss
        #pred: flattened DA preds
        #all_ap_predictions: a list of tensors. Each tensor contains the predictions of APs of each dialogue in the batch

    def unpad_features(self, features, lengths):
        #gets padded features from sequential encoder and returns only utts in each dialogue
        #(bs, max_seq_len, h) --> (bs*utts, h) , utts is the sum of actual len of each chunk (dialogue)
        
        node_features = []
        batch_size = features.size(0)
        for j in range(batch_size):
            cur_len = lengths[j].item()
            node_features.append(features[j, :cur_len, :])

        # node_features = torch.cat(node_features, dim=0).to(self.device)
        return node_features