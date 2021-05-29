import os
import random
import torch
import numpy as np
from model import Classifier


# utterance = namedtuple('utterance', ['speaker_id', 'text', 'tag1', 'tag2', 'tag3'])


# def process_file(dirname):
#     data = []
#     fnames = os.listdir(dirname)
#     for fname in fnames:
#         doc = []
#         with open(dirname+fname, 'r') as file:
#             reader = csv.reader(file)
#             for index, row in enumerate(reader):
#                 if index == 0:
#                     continue
#                 doc.append(row[8].split())
#                 if len(doc) == 200:
#                     data.append(doc)
#                     doc = []
#             if len(doc) > 0:
#                 data.append(doc)
#     data.append(doc)
#     print(len(data))
#     return data


def parse_pred(fname):
    data = []
    doc = []
    reader = open(fname, 'r')
    for row in reader:
        doc.append(row.strip())
        if len(doc) == 200:
            data.append(doc)
            doc = []
    if len(doc) > 0:
        data.append(doc)
    data.append(doc)
    print(len(data))
    return data


def get_batch(dialog):
    sent, ls, true_sents = [['<sos>']], [1], []
    for index, utterance in enumerate(dialog):
        true_sents.append(utterance)
        utter, _ = utterance.split('\t\t')
        utter = utter.split()
        if len(utter) < 200:
            sent.append(utter)
            ls.append(len(utter))
        else:
            sent.append(utter[:200])
            ls.append(200)
    ls = torch.LongTensor(ls)
    return true_sents, sent, ls


def evaluate(data, is_test=False):
    model.eval()
    pred_file = open("DA_labels_combined.txt", 'w')
    pred_file.write("TEXT\t\tBaseline\t\tRL Model\n")
    for doc in data:
        all_sents, sent, ls = get_batch(doc)
        if ls.size(0) < 3:
            continue
        if has_cuda:
            ls = ls.cuda()

        with torch.no_grad():
            # output = model.forward(sent, ls)
            output, _, _ = model.forward(sent, ls, is_test=True)
        output = output.squeeze()
        _, predict = torch.max(output, 1)
        y_pred = list(predict.cpu().numpy() if has_cuda else predict.numpy())
        assert(len(y_pred)) == len(all_sents)
        for sent, label in zip(all_sents, y_pred):
            pred_file.write(sent+'\t\t'+out_map[label]+'\n')


if __name__ == '__main__':
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
                 "r_Repeat,t1_self-talk,t3_3rd-party-talk,bh_Rhetorical-question Continue,bsc_Reject-part," \
                 "arp_Misspeak Self-Correction,bs_Reformulate/Summarize,f_Follow Me,qr_Or-Question,ft_Thanking," \
                 "g_Tag-Question,qo_Open-Question,bc_Correct-misspeaking,by_Sympathy,fw_Welcome".split(',')}
    print(labels_map)

    # out_tags = {'h': 0, 'bd': 1, 'rt': 2, 'fa': 3, 'qrr': 4, 'aa': 5, 'ft': 6, 'am': 7, 'r': 8, 't': 9, 'df': 10,
    #             'aap': 11, 't3': 12, '2': 13, 'g': 14, 'bc': 15, 'cs': 16, 'bh': 17, 'bsc': 18, 'cc': 19, 'bk': 20,
    #             'fh': 21, 's': 22, 'f': 23, 'qh': 24, 'fg': 25, 'tc': 26, 'br': 27, 'qw': 28, 'bs': 29, 'na': 30,
    #             'j': 31, 'arp': 32, 'fw': 33, 'by': 34, 'ar': 35, 'no': 36, 't1': 37, 'ba': 38, 'd': 39, 'qo': 40,
    #             'fe': 41, 'e': 42, 'bu': 43, 'qy': 44, 'b': 45, '%': 46, 'co': 47, 'ng': 48, 'm': 49, 'qr': 50, 'nd': 51}

    out_tags = {'b': 0, 'rt': 1, 'br': 2, 'fa': 3, 'ft': 4, 'cc': 5, 'arp': 6, 'm': 7, 's': 8, 'qrr': 9, 'aap': 10,
                'qy': 11, 'by': 12, 'bc': 13, 'ar': 14, 'bh': 15, 'aa': 16, 'fh': 17, 'nd': 18, 'e': 19, '%': 20,
                'j': 21, 'qo': 22, '2': 23, 'bd': 24, 'co': 25, 'g': 26, 'fe': 27, 'bk': 28, 'h': 29, 'qr': 30, 't': 31,
                'cs': 32, 'am': 33, 'fg': 34, 'bu': 35, 't1': 36, 'ng': 37, 'tc': 38, 'ba': 39, 'no': 40, 'na': 41,
                'df': 42, 'qh': 43, 'qw': 44, 'bsc': 45, 'f': 46, 'fw': 47, 'r': 48, 'd': 49, 't3': 50, 'bs': 51}

    assert len(out_tags) == len(labels_map)
    out_map = {out_tags[key]:labels_map[key] for key in out_tags}
    print(out_map)

    data = parse_pred('DA_labels.txt')

    prev_best_macro = 0.
    model = Classifier({'num_layers': 1, 'hidden_dim': 512, 'bidirectional': True, 'embedding_dim': 1024,
                        'dropout': 0.1, 'out_dim': len(out_map)})
    if has_cuda:
        model = model.cuda()
    model.init_weights()
    model.load_state_dict(torch.load('RL_model.pt'))
    evaluate(data)