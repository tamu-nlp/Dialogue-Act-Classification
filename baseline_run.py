import os
import random
import torch
import numpy as np
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


utterance = namedtuple('utterance', ['speaker_id', 'text', 'tag1', 'tag2', 'tag3'])


def process_file(dirname):
    data = []
    fnames = os.listdir(dirname)
    for fname in fnames:
        f = open(dirname+fname, 'r')
        doc = []
        for l in f:
            speaker_id, text, t1, t2, t3 = l.strip().split('|')
            doc.append(utterance(speaker_id, text.split(), t1, t2, t3))
            # doc.append(utterance(speaker_id, text.split(), t1, t2, t3))
            # if len(doc) == 100:
            #     data.append(doc)
            #     doc = []
        # if len(doc) > 0:
        #     data.append(doc)
        data.append(doc)
    return data


def get_data(fpath):
    return (process_file(fpath+'train/'),
            process_file(fpath+'val/'),
            process_file(fpath+'test/'))


def get_context(dialog, history_len):
    all_sent, all_ls = [], []
    sent, ls, out = [['<sos>'] for _ in range(history_len)], [1]*history_len, []
    for index, utterance in enumerate(dialog):
        out.append(out_map[utterance.tag3])
        sent.pop(0)
        ls.pop(0)
        if len(utterance.text) < 200:
            # TODO: Can use deque to improve time complexity if required
            sent.append(utterance.text)
            ls.append(len(utterance.text))
        else:
            sent.append(utterance.text[:200])
            ls.append(200)
        all_sent.append(deepcopy(sent))
        all_ls.append(deepcopy(ls))
    assert len(all_ls) == len(out) == len(all_sent)
    return all_sent, all_ls, out


def flatten_list(l):
    return [item for sample in l for item in sample]


def train(epoch, data, history_len, batch_size=50):
    random.shuffle(data)
    start_time = time.time()
    classifier_loss = 0
    optimizer.zero_grad()
    global prev_best_macro
    for ind, doc in enumerate(data):
        model.train()
        sent, ls, y_true = get_context(doc, history_len)
        seq_len = len(sent)
        for batch_index in range(0, len(sent), batch_size):
            sent_flat = flatten_list(sent[batch_index: min(batch_index + batch_size, seq_len)])
            ls_flat = flatten_list(ls[batch_index: min(batch_index + batch_size, seq_len)])

            ls_flat = torch.LongTensor(ls_flat)
            out = torch.LongTensor(y_true[batch_index: min(batch_index + batch_size, seq_len)])
            if has_cuda:
                ls_flat = ls_flat.cuda()
                out = out.cuda()

            output = model.forward(sent_flat, ls_flat, history_len)
            loss = criterion(output, out)  # last sentence is eod
            classifier_loss += loss.item()
            loss.backward()

        optimizer.step()
        optimizer.zero_grad()

    print("--Training--\nEpoch: ", epoch, "Discourse Act Classification Loss: ", classifier_loss,
          "Time Elapsed: ", time.time()-start_time)

    perf = evaluate(validate_data, history_len)
    if prev_best_macro < perf:
        prev_best_macro = perf
        print ("-------------------Test start-----------------------")
        _ = evaluate(test_data, history_len, True)
        print ("-------------------Test end-----------------------")
        print ("Started saving model")
        torch.save(model.state_dict(), '../model/baseline_model_5.pt')
        print("Completed saving model")


def evaluate(data, history_len, is_test=False, batch_size=50):
    y_true, y_pred = [], []
    model.eval()

    for doc in data:
        sent, ls, out = get_context(doc, history_len)
        y_true += out
        seq_len = len(sent)
        for batch_index in range(0, len(sent), batch_size):
            sent_flat = flatten_list(sent[batch_index: min(batch_index + batch_size, seq_len)])
            ls_flat = flatten_list(ls[batch_index: min(batch_index + batch_size, seq_len)])
            ls_flat = torch.LongTensor(ls_flat)
            if has_cuda:
                ls_flat = ls_flat.cuda()

            with torch.no_grad():
                output = model.forward(sent_flat, ls_flat, history_len)
            output = output.squeeze()
            _, predict = torch.max(output, 1)
            y_pred += list(predict.cpu().numpy() if has_cuda else predict.numpy())

    print("MACRO: ", precision_recall_fscore_support(y_true, y_pred, average='macro'))
    print("MICRO: ", precision_recall_fscore_support(y_true, y_pred, average='micro'))
    if is_test:
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Classification Report \n", classification_report(y_true, y_pred))
        print("Confusion Matrix \n", confusion_matrix(y_true, y_pred))
    return precision_recall_fscore_support(y_true, y_pred, average='macro')[2]


if __name__ == '__main__':

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--drop', help='DROP', default=6, type=float)
    parser.add_argument('--learn_rate', help='LEARNING RATE', default=0, type=float)
    parser.add_argument('--seed', help='SEED', default=0, type=int)
    parser.add_argument('--history', help='# Historical utterances to consider', default=5, type=int)

    args = parser.parse_args()
    has_cuda = torch.cuda.is_available()
    drop = args.drop
    learn_rate = args.learn_rate
    seed = args.seed
    history_len = args.history

    print ("[HYPERPARAMS] dropout: ", drop, "learning rate: ", learn_rate, "seed: ", seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if has_cuda:
        torch.cuda.manual_seed(seed)
    random.seed(seed)
    np.random.seed(seed)

    train_data, validate_data, test_data = get_data('../mrda_data/')
    print("Training Data: {0}, Validation Data: {1}, Test Data: {2}".format(len(train_data), len(validate_data), len(test_data)))
    # all_output_labels = set()
    # for elem in train_data:
    #     for utter in elem:
    #         all_output_labels.add(utter.tag3)
    out_map = {'tc': 0, 'h': 1, 'nd': 2, 'qw': 3, 'df': 4, 't1': 5, 'na': 6, 'cs': 7, 'qh': 8, 'by': 9, 'g': 10,
               'ng': 11, 'no': 12, 'bs': 13, 'fe': 14, 'rt': 15, 'd': 16, 't3': 17, 'fa': 18, 'br': 19, 'qrr': 20,
               'arp': 21, 'qr': 22, 'r': 23, 'aap': 24, '2': 25, 'e': 26, 'cc': 27, 'ba': 28, '%': 29, 'b': 30,
               'fw': 31, 'j': 32, 'bk': 33, 'bsc': 34, 's': 35, 'qo': 36, 'co': 37, 'bh': 38, 'aa': 39, 'ft': 40,
               'qy': 41, 'fh': 42, 'm': 43, 'ar': 44, 'f': 45, 'bc': 46, 'bu': 47, 't': 48, 'am': 49, 'fg': 50, 'bd': 51}

    print("All labels: ", out_map)
    prev_best_macro = 0.
    model = Classifier({'num_layers': 1, 'hidden_dim': 512, 'bidirectional': True, 'embedding_dim': 1024,
                        'dropout': drop, 'out_dim': len(out_map)})
    if has_cuda:
        model = model.cuda()
    model.init_weights()
    criterion = nn.CrossEntropyLoss()
    print("Model Created")

    params = filter(lambda p: p.requires_grad, model.parameters())
    optimizer = optim.Adam(params, lr=learn_rate, betas=[0.9, 0.999], eps=1e-8, weight_decay=0)

    try:
        for epoch in range(15):
            print("---------------------------Started Training Epoch = {0}--------------------------".format(epoch+1))
            train(epoch, train_data, history_len)

    except KeyboardInterrupt:
        print ("----------------- INTERRUPTED -----------------")
        # evaluate(validate_data, history_len)
        # evaluate(test_data, history_len, True)