import os
import random
import torch
import numpy as np
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import classification_report, confusion_matrix
from model import Classifier
import torch.nn as nn
import torch.optim as optim
import time
from collections import namedtuple


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
            if len(doc) == 100:
                data.append(doc)
                doc = []
        if len(doc) > 0:
            data.append(doc)
    return data


def get_data(fpath):
    return (process_file(fpath+'train/'), process_file(fpath+'val/'), process_file(fpath+'test/'))


def get_batch(dialog):
    sent, ls, out = [['<sos>']], [1], []
    for index, utterance in enumerate(dialog):
        out.append(out_map[utterance.tag3])
        if len(utterance.text) < 200:
            sent.append(utterance.text)
            ls.append(len(utterance.text))
        else:
            sent.append(utterance.text[:200])
            ls.append(200)

    ls = torch.LongTensor(ls)
    return sent, ls, out


def train(epoch, data, seed):
    random.shuffle(data)
    start_time = time.time()
    classifier_loss = 0
    parent_rl_loss = 0
    optimizer.zero_grad()
    global prev_best_macro

    for ind, doc in enumerate(data):
        model.train()
        sent, ls, y_true = get_batch(doc)
        if ls.size(0) < 3:
            continue
        out = torch.LongTensor(y_true)
        if has_cuda:
            ls = ls.cuda()
            out = out.cuda()

        output, critic_output, rl_loss = model.forward(sent, ls)
        temp_loss = criterion(output, out)  # last sentence is eod
        classifier_loss += temp_loss.item()
        loss = temp_loss

        output = output.squeeze()
        _, predict = torch.max(output, 1)
        y_pred = list(predict.cpu().detach().numpy() if has_cuda else predict.detach().numpy())
        reward = precision_recall_fscore_support(y_true, y_pred, average='macro')[2] + \
                 precision_recall_fscore_support(y_true, y_pred, average='micro')[2]

        critic_output = critic_output.squeeze()
        _, critic_predict = torch.max(critic_output, 1)
        y_pred_ground = list(critic_predict.cpu().detach().numpy() if has_cuda else critic_predict.detach().numpy())
        reward_ip = precision_recall_fscore_support(y_true, y_pred_ground, average='micro')[2] + \
                    precision_recall_fscore_support(y_true, y_pred_ground, average='macro')[2]

        loss += (reward.item(0) - reward_ip.item(0)) * rl_loss
        try:
            parent_rl_loss += rl_loss.item()
        except:
            pass

        loss.backward()
        if ind%20 == 19 or ind == len(data)-1:
            optimizer.step()
            optimizer.zero_grad()

    print("--Training--\nEpoch: ", epoch, "Discourse Act Classification Loss: ", classifier_loss, "Parent sentence loss: ",
          parent_rl_loss, "Time Elapsed: ", time.time()-start_time)

    perf = evaluate(validate_data)
    if prev_best_macro < perf:
        prev_best_macro = perf
        print ("-------------------Test start-----------------------")
        _ = evaluate(test_data, True)
        print ("-------------------Test end-----------------------")
        print ("Started saving model")
        torch.save(model.state_dict(), 'RL_model.pt')
        print("Completed saving model")


def evaluate(data, is_test=False):
    y_true, y_pred = [], []
    model.eval()

    for doc in data:
        sent, ls, out = get_batch(doc)
        if ls.size(0) < 3:
            continue
        if has_cuda:
            ls = ls.cuda()

        output, _, _ = model.forward(sent, ls, is_test=True)
        output = output.squeeze()
        _, predict = torch.max(output, 1)
        y_pred += list(predict.cpu().numpy() if has_cuda else predict.numpy())
        y_true += out

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

    args = parser.parse_args()
    has_cuda = torch.cuda.is_available()
    drop = args.drop
    learn_rate = args.learn_rate
    seed = args.seed
    print ("[HYPERPARAMS] dropout: ", drop, "learning rate: ", learn_rate, "seed: ", seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if has_cuda:
        torch.cuda.manual_seed(seed)
    random.seed(seed)
    np.random.seed(seed)

    train_data, validate_data, test_data = get_data('../mrda_data/')
    print("Training Data: {0}, Validation Data: {1}, Test Data: {2}".format(len(train_data), len(validate_data), len(test_data)))
    all_output_labels = set()
    for elem in train_data:
        for utter in elem:
            all_output_labels.add(utter.tag3)
    out_map = {elem:id for id,elem in enumerate(list(all_output_labels))}
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
            train(epoch, train_data, seed)

    except KeyboardInterrupt:
        print ("----------------- INTERRUPTED -----------------")
        evaluate(validate_data)
        evaluate(test_data)