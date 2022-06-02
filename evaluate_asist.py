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

print("device ", device)


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
            label = get_single_da_label(label)
            text = utt if ASR else cor_utt
            if label == "z" or label == "x": continue
            if label == "bh": label = "b" #in MRDA, after cleaning, we do not have a bh left
            if label == "s^d^g": label = "s"

            doc.append(utterance(speaker_id, text, label, AP))
        dataset.append(doc)
    return dataset

def get_single_da_label(raw_da_tag):
    keep_spec_tags_list = ['no', 'cs', 'fe', 't1', 't3', 't', 'j', 'bu', 'ba', 'e', 'fa', 'ft', 'br', "2", 'f', 'bd', 'r', 'tc',"by", 'aa',
                         "ar", 'cc', 'cs', 'df', 'bc', 'bs']
    keep_spec_tags_list_quest = ['br', 'bd', 'bu', 'cs']
    tag = raw_da_tag.split(":")
    tag = tag[0] #for Quotes: DA on left is for entire utts
    tag = re.sub(" ", "", tag)
    spl = tag.split("|")
    pipe_das = []
    for value in spl:
        #if a floor mechanism, skip
        if value in ["fh", "h", "fg"] and len(spl) > 1: continue
        org_value = value
        #get rid of interuptions at the end
        value = re.sub("\.(%--|%-|%|x)", "", value) #some utterances have s.x
        # value = re.sub("\^j|\^rt|\^t1|\^t3|\^fe|\^tc|\^t", "", value) #getting rid of some tags
        value = re.sub("\^rt", "", value) #getting rid of rt tags


        #merge labels
        value = re.sub("^(%--|%-|%)", "%", value) #x, %, %-, %-- 
        value = re.sub("bk", "aa", value) #merging <bk> and <aa>
        value = re.sub("\^m", "^r", value) #merging <r> and <m>
        value = re.sub("\^(aap|na)(?![a-z])", "^aa", value) #aap|na --> aa
        value = re.sub("\^co(?![a-z])", "^cs", value) #co --> cs
        value = re.sub("\^(arp|nd|ng)(?![a-z])", "^ar", value) #arp|nd|ng --> ar
        value = re.sub("qh", "qy", value) #merging <qh> and <qy>
        value = re.sub("qo", "qw", value) #merging <qo> and <qw>
        value = re.sub("qr(?![a-z])", "qy", value) #merging <qr> and <qy> #keeping qrr
        value = re.sub("bsc", "bc", value) #merging <bsc> and <bc>

        #handle standalone specific tags with <s>
        tags = value.split("^")
        if tags[0] == "s" and len(tags) == 2: #s^-
            if tags[1] in keep_spec_tags_list: 
                value = tags[1]
                pipe_das.append(value)
                continue
        if value == "s^t^tc": 
            pipe_das.append("tc")
            continue

        #fix, if s^tc^t occur together, don't reduce to <s>, fixed
        value = re.sub("\^j|\^rt|\^t1|\^t3|\^fe|\^tc|\^t|\^r|\^fw|\^fa|\^by", "", value) #getting rid of some tags if they do not occur with <s> only


        #reduce labels
        #match from start else "s^cs^na" matches s^na
        #don't need to check for <r> now
        value = re.sub("^s\^bd\^no(?![a-z]|\^)", "bd", value) #s^bd^no --> bd
        value = re.sub("^s\^bd\^df(?![a-z]|\^)", "bd", value) #s^bd^df --> bd
        value = re.sub("^s\^ba\^aa(?![a-z]|\^)", "ba", value) #s^ba^aa --> ba
        value = re.sub("^s\^cs\^aa(?![a-z]|\^)", "cs", value) #s^cs^aa --> cs
        value = re.sub("^s\^bu\^e(?![a-z]|\^)", "bu", value) #s^bu^e --> bu
        value = re.sub("^s\^df\^ar(?![a-z]|\^)", "ar", value) #s^df^ar --> ar
        value = re.sub("^s\^df\^aa(?![a-z]|\^)", "aa", value) #s^df^aa --> aa
        value = re.sub("^s\^df\^e(?![a-z]|\^)", "df", value) #s^df^aa --> aa
        value = re.sub("^s\^cs\^e(?![a-z]|\^)", "cs", value) #s^cs^e --> cs

        value = re.sub("^(fh|fg|h)(?![a-z]|\^)", "fl", value) #(fh|fg|h) --> fl

        value = re.sub("^qy\^f(?![a-z]|\^)", "f", value) #qy^f --> f
        value = re.sub("^qy\^bu\^d(?![a-z]|\^)", "bu", value) #qy^bu^d --> bu
        value = re.sub("^qy\^bu(?![a-z]|\^)", "bu", value) #qy^bu --> bu
        value = re.sub("^qy\^d\^g(?![a-z]|\^)", "qy", value) #qy^d^g --> qy
        value = re.sub("^(s|qy|qw|qrr)\^cs\^(j|e)(?![a-z]|\^)", "cs", value) #-^cs^(j|e) --> cs


        # #handle standalone specific tags with <s>
        tags = value.split("^")
        if tags[0] == "s" and len(tags) == 2: #s^-
            if tags[1] in keep_spec_tags_list: value = tags[1]
            else: value = tags[0] ##??

        if tags[0][0] == "q" and len(tags) == 2: #question^-
            if tags[1] in keep_spec_tags_list_quest: value = tags[1] 
            else: value = tags[0] 


        value = apply_precedence(value)
        
        if value == "" : 
            continue

        # if value in pattern_count_split_rem: pattern_count_split_rem[value] += 1    
        # else: pattern_count_split_rem[value] = 1
        pipe_das.append(value)
    
    if len(pipe_das) == 1:
        value = pipe_das[0]
    else: #pick best from both
        for i in range(len(pipe_das)): pipe_das[i] = "^"+pipe_das[i]
        value = apply_precedence(" ".join(pipe_das))
    
    return value


def apply_precedence(value):
    #(cc, cs) > bu> bd > ba > (ar, aa) >  (am, no) > df > 2> e|f > bs|bc > s|(qy, qw, qrr)
    #apply precedence rules
    if "^cs" in value: value = "cs"
    elif "^cc" in value: value = "cc"
    elif "^bu" in value: value = "bu"
    elif "^bd" in value: value = "bd"
    elif "^ba" in value: value = "ba"
    elif "^ar" in value: value = "ar"
    elif "^aa" in value: value = "aa"
    elif "^bu" in value: value = "bu"
    elif "^am" in value: value = "am"
    elif "^no" in value: value = "no"
    elif "^df" in value: value = "df"
    elif "2" in value: value = "2"
    elif "^e" in value: value = "e"
    elif "^f" in value: value = "f"
    elif "^br" in value: value = "br"
    elif "^bs" in value: value = "bs"
    elif "^bc" in value: value = "bc"
    elif "qy" in value: value = "qy"
    elif "qw" in value: value = "qw"
    elif "qrr" in value: value = "qy" #for now
    elif "^b" in value: value = "b"
    elif "^bh" in value: value = "bh"
    elif "^t1" in value: value = "t1"
    elif "^tc" in value: value = "tc"
    elif "^s" in value: value = "s"
    return value


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


    new_map = {'2': '%', '5': '2', '0': 'aa', '30': 'am', '9': 'ar', '4': 'b', '18': 'ba', '23': 'bc', '24': 'bd', '29': 'br',
    '28': 'bs', '17': 'bu', '31': 'by', '10': 'cc', '11': 'cs', '8': 'df', '6': 'e', '22': 'f', '20': 'fa', '27': 'fe', 
    '7': 'fl', '26': 'ft', '19': 'j', '14': 'no', '16': 'qw', '15': 'qy', '3': 'r', '1': 's', '12': 't', '21': 't1', 
    '25': 't3', '13': 'tc', '32': 'qrr'}

    tag_desc_map = {'tc': 'Topic Change', 'qw':'Wh-Question','df':'Defending/Explanation','t1':'Self Talk'
    ,'cs':'Suggestion','by':'Sympathy', 'qrr':'Or Clause After Y/N Question'
    ,'no':'No Knowledge','bs':'Summary','fe':'Exclamation','t3':'Third Party Talk','fa':'Apology','br':'Repetition Request','r':'Repeat'
    ,'2':'Collaborative Completion','e':'Elaboration','cc':'Commitment','ba':'Assessment/Appreciation','%':'Disruption','b':'Backchannel'
    ,'fw':'Welcome','j':'Joke','s':'Statement'
    ,'aa':'Accept','ft':'Thanks','qy':'Y/N Question','fl':'Floor mechanism','m':'Mimic','ar':'Reject','f':"Follow Me"
    ,'bc':'Correct Misspeaking','bu':'Understanding Check','t':'About-Task','am':'Maybe','bd':'Downplayer'  
    }

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


    args = parser.parse_args()
    has_cuda = torch.cuda.is_available()
    ASR = args.ASR
    data_path = args.data
    results_filename = args.results_file

    saved_model_file = '../model/seq_baseline_roberta_cleaned_B64_W16_seed1.pt'
    test_data = get_data(data_path, ASR)

    print("Test Data: {0}".format(len(test_data)))

    out_map = {'%': 2,'2': 5, 'aa': 0, 'am': 30, 'qrr': 32,
    'ar': 9, 'b': 4, 'ba': 18, 'bc': 23, 'bd': 24, 'br': 29, 'bs': 28,'bu': 17,'by': 31,
    'cc': 10,'cs': 11,'df': 8,'e': 6, 'f': 22,'fa': 20,'fe': 27,'fl': 7,'ft': 26,'j': 19,
    'no': 14,'qw': 16,'qy': 15,'r': 3,'s': 1,'t': 12,'t1': 21,'t3': 25,'tc': 13}
    print("All labels: ", len(out_map))
    model = Classifier({'num_layers': 1, 'hidden_dim': 512, 'bidirectional': True, 'embedding_dim': 768,
                        'dropout': 0.1, 'out_dim': len(out_map)})

    model = model.to(device)
    model.init_weights()
    model.load_state_dict(torch.load(saved_model_file))
    evaluate(test_data, window_size=16, batch_size=64, results_filename = results_filename)