import torch
from baseline_model import Classifier


def get_context(dialog, history_len):
    all_sent, all_ls = [], []
    unchanged_sents = []
    sent, ls = [['<sos>'] for _ in range(history_len)], [1]*history_len
    for index, utterance in enumerate(dialog):
        # out.append(out_map[utterance.tag3])
        unchanged_sents.append(utterance)
        sent.pop(0)
        ls.pop(0)
        _utter = utterance.split('\t\t')[0]
        utter = _utter.split()
        if len(utter) < 200:
            # TODO: Can use deque to improve time complexity if required
            sent.append(utter)
            ls.append(len(utter))
        else:
            sent.append(utter[:200])
            ls.append(200)
        all_sent.append(deepcopy(sent))
        all_ls.append(deepcopy(ls))
    assert len(all_ls) == len(all_sent)
    return all_sent, all_ls, unchanged_sents
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
    # doc = []
    reader = open(fname, 'r')
    for row in reader:
        # doc.append(row.strip())
        # if len(doc) == 200:
        #     data.append(doc)
        #     doc = []
    # if len(doc) > 0:
    #     data.append(doc)
        data.append(row.strip())
    # data.append(doc)
    print(len(data))
    return data


def flatten_list(l):
    return [item for sample in l for item in sample]


def evaluate(data, history_len, batch_size):
    model.eval()
    pred_file = open("../model/DA_labels_new.txt", 'w')

    all_sent, all_ls, unchanged_sents = get_context(data, history_len)
    seq_len = len(all_sent)
    y_pred, y_score = [], []
    for batch_index in range(0, len(all_sent), batch_size):
        sent_flat = flatten_list(all_sent[batch_index: min(batch_index + batch_size, seq_len)])
        ls_flat = flatten_list(all_ls[batch_index: min(batch_index + batch_size, seq_len)])
        ls_flat = torch.LongTensor(ls_flat)
        if has_cuda:
            ls_flat = ls_flat.cuda()

        with torch.no_grad():
            output = model.forward(sent_flat, ls_flat, history_len)

        # output = output.squeeze()
        output = torch.nn.functional.softmax(output, dim=1)
        score, predict = torch.max(output, 1)
        # print(predict, score)
        y_pred += list(predict.cpu().numpy() if has_cuda else predict.numpy())
        y_score += list(score.cpu().numpy() if has_cuda else score.numpy())
    print(len(y_pred), len(y_score), len(unchanged_sents))
    assert len(y_pred) == len(y_score) == len(unchanged_sents)

    length_list = [len(row) for row in unchanged_sents]
    column_width = max(length_list)

    for i,sent in enumerate(unchanged_sents):
        if out_map[y_pred[i]] != ' ':
            pred_file.write('\t\t'.join([sent, out_map[y_pred[i]]+' ('+str(y_score[i])+')'])+'\n')
        else:
            pred_file.write('\t\t'.join([sent,'-'])+'\n')


if __name__ == '__main__':
    has_cuda = torch.cuda.is_available()

    np.random.seed(0)
    torch.manual_seed(0)
    if has_cuda:
        torch.cuda.manual_seed(0)
    random.seed(0)
    np.random.seed(0)

    labels_map = {elem.split('_')[0]:elem.split('_')[1] for elem in "s_ ,b_Backchannel,fh_Floor Holder,bk_Acknowledgement,aa_Accept,df_Defending/Explanation," \
                 "e_Elaboration,%_Interrupted/Abandoned/Uninterpretable,rt_Rising Tone,fg_Floor Grabber," \
                 "cs_Suggestion,ba_Assessment/Appreciation,bu_Understanding Check,d_Declarative-Question,na_Affirmative Answers," \
                 "qw_Wh-Question,ar_Reject,2_Collaborative Completion,no_No Knowledge,h_Hold," \
                 "co_Command,qy_Yes-No-question,nd_Dispreferred Answers,j_Joke,bd_Downplayer," \
                 "cc_Commitment,ng_Negative Answers,am_Maybe,qrr_Or Clause After Y/N Question,fe_Exclamation,m_Mimic,fa_Apology," \
                 "t_About-task,br_Repition Request,aap_Partial Accept,qh_Rhetorical-Question,tc_Topic Change," \
                 "r_Repeat,t1_self-talk,t3_3rd-party-talk,bh_Rhetorical Question Backchannel,bsc_Partial Reject," \
                 "arp_Self-Correct Misspeaking,bs_Summary,f_Follow Me,qr_Or-Question,ft_Thanks," \
                 "g_Tag-Question,qo_Open-ended Question,bc_Correct-misspeaking,by_Sympathy,fw_Welcome".split(',')}
    print(labels_map)

    # out_tags = {'h': 0, 'bd': 1, 'rt': 2, 'fa': 3, 'qrr': 4, 'aa': 5, 'ft': 6, 'am': 7, 'r': 8, 't': 9, 'df': 10,
    #             'aap': 11, 't3': 12, '2': 13, 'g': 14, 'bc': 15, 'cs': 16, 'bh': 17, 'bsc': 18, 'cc': 19, 'bk': 20,
    #             'fh': 21, 's': 22, 'f': 23, 'qh': 24, 'fg': 25, 'tc': 26, 'br': 27, 'qw': 28, 'bs': 29, 'na': 30,
    #             'j': 31, 'arp': 32, 'fw': 33, 'by': 34, 'ar': 35, 'no': 36, 't1': 37, 'ba': 38, 'd': 39, 'qo': 40,
    #             'fe': 41, 'e': 42, 'bu': 43, 'qy': 44, 'b': 45, '%': 46, 'co': 47, 'ng': 48, 'm': 49, 'qr': 50, 'nd': 51}

    out_tags = {'tc': 0, 'h': 1, 'nd': 2, 'qw': 3, 'df': 4, 't1': 5, 'na': 6, 'cs': 7, 'qh': 8, 'by': 9, 'g': 10,
                'ng': 11, 'no': 12, 'bs': 13, 'fe': 14, 'rt': 15, 'd': 16, 't3': 17, 'fa': 18, 'br': 19, 'qrr': 20,
                'arp': 21, 'qr': 22, 'r': 23, 'aap': 24, '2': 25, 'e': 26, 'cc': 27, 'ba': 28, '%': 29, 'b': 30,
                'fw': 31, 'j': 32, 'bk': 33, 'bsc': 34, 's': 35, 'qo': 36, 'co': 37, 'bh': 38, 'aa': 39, 'ft': 40,
                'qy': 41, 'fh': 42, 'm': 43, 'ar': 44, 'f': 45, 'bc': 46, 'bu': 47, 't': 48, 'am': 49, 'fg': 50, 'bd': 51}


    assert len(out_tags) == len(labels_map)
    out_map = {out_tags[key]:labels_map[key] for key in out_tags}
    print(out_map)

    data = parse_pred('../model/DA_labels_new_1.txt')

    prev_best_macro = 0.
    model = Classifier({'num_layers': 1, 'hidden_dim': 512, 'bidirectional': True, 'embedding_dim': 1024,
                        'dropout': 0.1, 'out_dim': len(out_map)})
    if has_cuda:
        model = model.cuda()
    model.init_weights()
    model.load_state_dict(torch.load('../model/baseline_model_15.pt'))
    evaluate(data, history_len=15, batch_size=10)