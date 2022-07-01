import os
import random
import torch
import numpy as np
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import classification_report, confusion_matrix
from baseline_model import Classifier
import csv
from collections import namedtuple
import warnings
warnings.filterwarnings('ignore')
if torch.cuda.is_available():     
    device = torch.device("cuda:0")
else:
    device = torch.device("cpu")

#predicts DA labels on ASIST data in csv format
def process_file(dirname):
    print('baseline_predict.process_file' + dirname)
    data = []
    fnames = os.listdir(dirname)
    for fname in fnames:
        doc = []
        with open(dirname+fname, 'r') as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader):
                if index == 0:
                    continue
                doc.append(row[8])
                if len(doc) == 200:
                    data.append(doc)
                    doc = []
            if len(doc) > 0:
                data.append(doc)
    data.append(doc)
    # print(len(data))
    return data


def get_batch(dialog):
    print('baseline_predict.get_batch')
    sent, true_sents = [], []
    for index, utterance in enumerate(dialog):
        sent.append(utterance[:200])
    return true_sents, sent


def evaluate(data, is_test=False):
    print('baseline_predict.evaluate')
    model.eval()
    pred_file = open("DA_labels.txt", 'w')
    for doc in data:
        all_sents, sent = get_batch(doc)
        if len(sent) < 3:
            continue

        with torch.no_grad():
            output = model.forward(sent)
        _, predict = torch.max(output, 1)
        y_pred = list(predict.cpu().numpy() if torch.cuda.is_available() else predict.numpy())
        for sent, label in zip(sent, y_pred):
            pred_file.write(sent+'\t\t'+out_map[label]+'\n')


if __name__ == '__main__':
    print('baseline_predict.__main__')
    has_cuda = torch.cuda.is_available()

    np.random.seed(0)
    torch.manual_seed(0)
    if has_cuda:
        torch.cuda.manual_seed(0)
    random.seed(0)
    np.random.seed(0)

    labels_map = {elem.split('_')[0]:elem.split('_')[1] for elem in "s_Statement,b_Continuer,fh_Floor Holder,bk_Acknowledge-answer,aa_Accept,df_Defending/Explanation," \
                 "e_Expansions of y/n Answers,%_Interrupted/Abandoned/Uninterpretable,rt_Rising Tone,fg_Floor Grabber," \
                 "cs_Offer,ba_Assessment/Appreciation,bu_Understanding Check,d_Declarative-Question,na_Affirmative Non-yes Answers," \
                 "qw_Wh-Question,ar_Reject,2_Collaborative Completion,no_Other Answers,h_Hold Before Answer/Agreement," \
                 "co_Action-directive,qy_Yes-No-question,nd_Dispreferred Answers,j_Humorous Material,bd_Downplayer," \
                 "cc_Commit,ng_Negative Non-no Answers,am_Maybe,qrr_Or-Clause,fe_Exclamation,m_Mimic Offer,fa_Apology," \
                 "t_About-task,br_Signal-non-understanding,aap_Accept-part,qh_Rhetorical-Question,tc_Topic Change," \
                 "r_Repeat,t1_Self-talk,t3_3rd-party-talk,bh_Rhetorical-question Continue,bsc_Reject-part," \
                 "arp_Misspeak Self-Correction,bs_Reformulate/Summarize,f_Follow Me,qr_Or-Question,ft_Thanking," \
                 "g_Tag-Question,qo_Open-Question,bc_Correct-misspeaking,by_Sympathy,fw_Welcome".split(',')}
    # print(labels_map)

    out_tags = {'h': 0, 'bd': 1, 'rt': 2, 'fa': 3, 'qrr': 4, 'aa': 5, 'ft': 6, 'am': 7, 'r': 8, 't': 9, 'df': 10,
                'aap': 11, 't3': 12, '2': 13, 'g': 14, 'bc': 15, 'cs': 16, 'bh': 17, 'bsc': 18, 'cc': 19, 'bk': 20,
                'fh': 21, 's': 22, 'f': 23, 'qh': 24, 'fg': 25, 'tc': 26, 'br': 27, 'qw': 28, 'bs': 29, 'na': 30,
                'j': 31, 'arp': 32, 'fw': 33, 'by': 34, 'ar': 35, 'no': 36, 't1': 37, 'ba': 38, 'd': 39, 'qo': 40,
                'fe': 41, 'e': 42, 'bu': 43, 'qy': 44, 'b': 45, '%': 46, 'co': 47, 'ng': 48, 'm': 49, 'qr': 50, 'nd': 51}

    assert len(out_tags) == len(labels_map)
    out_map = {out_tags[key]:labels_map[key] for key in out_tags}
    # print(out_map)

    data = process_file('../asist_data/')

    prev_best_macro = 0.
    model = Classifier({'num_layers': 1, 'hidden_dim': 512, 'bidirectional': True, 'embedding_dim': 768,
                            'dropout': 0.1, 'out_dim': len(out_map), "sum_emb_rep": False})
    model = model.to(device)
    model.init_weights()
    model.load_state_dict(torch.load('../model/sequential_baseline_roberta_B32_W8_seed1.pt'))
    #update filepath to saved model weights
    evaluate(data)
