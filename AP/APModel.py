import torch
import numpy as np
from APClassifier import JointClassifier
from copy import deepcopy

class Predictor:
    def __init__(self, model_path, history_len):
        super(Predictor, self).__init__()

        self.history_len = history_len
        gpu_id = 'cuda:0'
        if torch.cuda.is_available():     
            device = torch.device(gpu_id)
        else:
            device = torch.device("cpu")

        self.device = device
        config = {'hidden_dim': 400, 'bidirectional': True, 'embedding_dim': 768,
                            'dropout': 0.4, 'out_dim_part':3, 'device': device,
                            'use_CLS': True, 'ASIST' : True, 
                            
                        'embedding_config': {'model_type':'roberta-base',
                        'device': device, 'nfinetune': 0,
                        'sum_hidden_states': False},
                    }

        model = JointClassifier(config)
        model = model.to(device)
        pretrained_dict = torch.load(model_path, map_location=device)
        self.model = model
        self.model.load_state_dict(pretrained_dict, strict = False)
        self.model = self.model.eval()
        print("Model Created")

        self.reset()

    def reset(self):
        self.text_len_tensor = torch.tensor([self.history_len])
        self.text_raw = ["<sos>" for _ in range(self.history_len)]
        self.last_spk = None
        self.speaker_list = [0] * self.history_len #contains a tensor of spk ids
        self.spk_map = {}

    def predict(self, curr_spk, utterance):
        if curr_spk not in self.spk_map: self.spk_map[curr_spk] = len(self.spk_map)
        spk = '<same> ' if curr_spk == self.last_spk else '<switch> '
        self.text_raw.pop(0)
        self.text_raw.append(spk + deepcopy(utterance))
        self.last_spk = curr_spk
        self.speaker_list.pop(0)
        self.speaker_list.append(self.spk_map[curr_spk])

        data = {
            'text_raw': [self.text_raw],
            'speaker_list': [torch.tensor(self.speaker_list).to(self.device)],
            'text_len_tensor': torch.tensor([self.history_len]).to(self.device),
        }

        with torch.no_grad():
            _, pred, _ = self.model(data, get_loss = False)
            pred = pred[0] #since we only have one dialogue being processed at a time

        label = pred[-1] #the last utterance label

        label_map = {0: "A", 1:"B", 2:"None"}

        return {"part": label_map[label.item()],
                "connect": 1}


        