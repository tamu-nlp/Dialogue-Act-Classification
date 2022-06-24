from cProfile import label
import os
import torch
import numpy as np
import pandas as pd
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import classification_report, confusion_matrix
from baseline_model import Classifier
import torch.nn as nn
import torch.optim as optim
import time
from copy import deepcopy
from collections import namedtuple
np.set_printoptions(threshold=np.inf)
from sklearn.metrics import accuracy_score
import regex as re
import warnings
warnings.filterwarnings('ignore')
if torch.cuda.is_available():     
    device = torch.device("cuda:0")
else:
    device = torch.device("cpu")

print("Evaluating on ", device)


utterance = namedtuple('utterance', ['speaker_id', 'text', 'label', "AP"])


def process_file(dirname, ASR):
    dataset = []
    fnames = os.listdir(dirname)
    for fname in fnames:
        data = pd.read_csv(os.path.join(dirname,fname), sep = "#", header=None, 
                 names = ["speaker", 'utt', 'corr_utt', 'DA', 'AP'])
        doc = []
        for i in range(len(data)):
            cor_utt = data.iloc[i].corr_utt
            utt = data.iloc[i].utt
            AP = data.iloc[i].AP
            speaker_id = data.iloc[i].speaker
            label = data.iloc[i].DA
            # org_label = label
            label = get_single_da_label(label)
            text = utt if ASR else cor_utt
            if label == "z" or label == "x": continue
            if label == "aa6r": label = "aa" #a typo

            doc.append(utterance(speaker_id, text, label, AP))
        dataset.append(doc)
    return dataset

def get_single_da_label(raw_da_tag):
    tag = raw_da_tag.split(":")
    tag = tag[0] #for Quotes: DA on left is for entire utts
    tag = re.sub(" ", "", tag)
    label = tag.split("|")[0]
    label = label.split('.')[0] #removing disruptions
    if any(char in ['^'] for char in label):
        return label.split('^')[1] #pick first specific tag, if such exists
    else: return label #else the general tag



def get_data(fpath, ASR):
    return (process_file(fpath, ASR))


def get_context(dialog):
    all_sent = []
    out = []
    last_spk = 'None'
    for index, utterance in enumerate(dialog):
        out.append(out_map[utterance.label])
        cur_speaker = utterance.speaker_id
        spk = '<same> ' if cur_speaker == last_spk else '<switch> '
        all_sent.append(spk + deepcopy(utterance.text[:300]))
        last_spk = cur_speaker

    assert len(out) == len(all_sent)
    return all_sent, out
        

def evaluate(data, window_size, batch_size=100, results_filename = "results"):
    y_true, y_pred = [], []
    model.eval()

    for doc in data:
        sent, out = get_context(doc)
        y_true += out
        seq_len = len(sent)
        for batch_index in range(0, len(sent), batch_size):
            sent_flat = sent[max(0, batch_index-window_size) : min(batch_index + batch_size, seq_len)]
            # out_flat = np.array(out[max(0, batch_index) : min(batch_index + batch_size, seq_len)]) #prob?

            with torch.no_grad():
                output = model.forward(sent_flat)
            _, predict = torch.max(output, 1)
            start_index = 0 if batch_index == 0 else window_size
            predict = predict[start_index:].cpu().numpy() if has_cuda else predict.numpy()
            y_pred += list(predict)
            


    # macro_ = precision_recall_fscore_support(y_true, y_pred, average='macro')[2]
    print("MACRO: ", precision_recall_fscore_support(y_true, y_pred, average='macro'))
    print("MICRO: ", precision_recall_fscore_support(y_true, y_pred, average='micro'))
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Classification Report \n", classification_report(y_true, y_pred))
    # print("Confusion Matrix \n", confusion_matrix(y_true, y_pred))
    macro_f1_da = precision_recall_fscore_support(y_true, y_pred, average='macro')[2]
    print(classification_report(y_true, y_pred)[0])

    dict_report = classification_report(y_true, y_pred, output_dict=True)


    new_map = {'0': 'tc', '1': 'h', '2': 'nd', '3': 'qw', '4': 'df', '5': 't1', '6': 'na', 
    '7': 'cs', '8': 'qh', '9': 'by', '10': 'g', '11': 'ng', '12': 'no', '13': 'bs', '14': 'fe', 
    '15': 'rt', '16': 'd', '17': 't3', '18': 'fa', '19': 'br', '20': 'qrr', '21': 'arp', 
    '22': 'qr', '23': 'r', '24': 'aap', '25': '2', '26': 'e', '27': 'cc', '28': 'ba', '29': '%', 
    '30': 'b', '31': 'fw', '32': 'j', '33': 'bk', '34': 'bsc', '35': 's', '36': 'qo', '37': 'co',
    '38': 'bh', '39': 'aa', '40': 'ft', '41': 'qy', '42': 'fh', '43': 'm', '44': 'ar', '45': 'f',
    '46': 'bc', '47': 'bu', '48': 't', '49': 'am', '50': 'fg', '51': 'bd'}

    tag_desc_map = {'s': 'Statement', 'b': 'Backchannel', 'fh': 'Floor Holder', 'bk': 'Acknowledgement', 'aa': 'Accept', 
    'df': 'Defending/Explanation', 'e': 'Elaboration', '%': 'Interrupted/Uninterpretable', 'rt': 'Rising Tone', 
    'fg': 'Floor Grabber', 'cs': 'Suggestion', 'ba': 'Appreciation', 'bu': 'Understanding Check', 
    'd': 'Declarative-Question', 'na': 'Affirmative Answer', 'qw': 'Wh-Question', 'ar': 'Reject', 
    '2': 'Collaborative Completion', 'no': 'No Knowledge', 'h': 'Hold Before Answer', 'co': 'Command', 
    'qy': 'Yes-No-question', 'nd': 'Dispreferred Answers', 'j': 'Humorous Material', 'bd': 'Downplayer', 
    'cc': 'Commitment', 'ng': 'Negative Answer', 'am': 'Maybe', 'qrr': 'Or Clause After Y/N Question', 'fe': 'Exclamation',
    'm': 'Mimic', 'fa': 'Apology', 't': 'About-task', 'br': 'Repetition Request', 'aap': 'Partial Accept', 
    'qh': 'Rhetorical-Question', 'tc': 'Topic Change', 'r': 'Repeat', 't1': 'Self-talk', 't3': '3rd-party-talk', 
    'bh': 'Rhetorical Question Backchannel', 'bsc': 'Self-Correct Misspeaking', 'arp': 'Partial Reject', 'bs': 'Summary',
    'f': 'Follow Me', 'qr': 'Or-Question', 'ft': 'Thanking', 'g': 'Tag-Question', 'qo': 'Open-ended Question',
    'bc': 'Correct-misspeaking', 'by': 'Sympathy', 'fw': 'Welcome'}

    fileOpen = open(results_filename+'.csv', 'w')
    fileOpen.write('id,tag,desc,precision,recall,F1,support\n') 
    for key, value in dict_report.items():
        if len(key) > 2: continue
        tag = new_map[str(key)]
        fileOpen.write(str(key)+','+tag+','+ tag_desc_map[tag]+','+ str(round(value['precision'], 4))+','+str(round(value['recall'], 4))+','+str(round(value['f1-score'],4))+','+str(value['support'])+'\n')

    fileOpen.close()

    return macro_f1_da


if __name__ == '__main__':
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--data', help='Path to folder containing the data', default="../asist_data/", type=str)
    parser.add_argument('--results_file', help='Name of file to write classwise results to', default="results", type=str)
    parser.add_argument('--ASR', help='Use uncorrected ASR transcripts', default=0, type=int)
    parser.add_argument('--model_file', help='The trained model weights file to use', default='sequential_baseline_roberta_B32_W8_seed1.pt', type=str)


    args = parser.parse_args()
    has_cuda = torch.cuda.is_available()
    ASR = args.ASR
    data_path = args.data
    results_filename = args.results_file
    saved_model_file = args.model_file

    test_data = get_data(data_path, ASR)

    print("Test Data: {0}".format(len(test_data)))

    out_map = {'tc': 0, 'h': 1, 'nd': 2, 'qw': 3, 'df': 4, 't1': 5, 'na': 6, 'cs': 7, 'qh': 8, 'by': 9, 'g': 10,
                'ng': 11, 'no': 12, 'bs': 13, 'fe': 14, 'rt': 15, 'd': 16, 't3': 17, 'fa': 18, 'br': 19, 'qrr': 20,
                'arp': 21, 'qr': 22, 'r': 23, 'aap': 24, '2': 25, 'e': 26, 'cc': 27, 'ba': 28, '%': 29, 'b': 30,
                'fw': 31, 'j': 32, 'bk': 33, 'bsc': 34, 's': 35, 'qo': 36, 'co': 37, 'bh': 38, 'aa': 39, 'ft': 40,
                'qy': 41, 'fh': 42, 'm': 43, 'ar': 44, 'f': 45, 'bc': 46, 'bu': 47, 't': 48, 'am': 49, 'fg': 50, 'bd': 51}
    print("All labels: ", len(out_map))
    model = Classifier({'num_layers': 1, 'hidden_dim': 512, 'bidirectional': True, 'embedding_dim': 768,
                        'dropout': 0.1, 'out_dim': len(out_map), "sum_emb_rep": False})

    model = model.to(device)
    model.init_weights()
    model.load_state_dict(torch.load(saved_model_file))
    evaluate(test_data, window_size=8, batch_size=32, results_filename = results_filename)
