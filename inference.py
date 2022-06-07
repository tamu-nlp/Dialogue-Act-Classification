import torch
from baseline_model import Classifier
from copy import deepcopy
if torch.cuda.is_available():     
    device = torch.device("cuda")
else:
    device = torch.device("cpu")


labels_map = {elem.split('_')[0]:elem.split('_')[1] for elem in "s_Statement,b_Backchannel,fh_Floor Holder,bk_Acknowledgement,aa_Accept,df_Defending/Explanation," \
             "e_Elaboration,%_Interrupted/Abandoned/Uninterpretable,rt_Rising Tone,fg_Floor Grabber," \
             "cs_Suggestion,ba_Assessment/Appreciation,bu_Understanding Check,d_Declarative-Question,na_Affirmative Answers," \
             "qw_Wh-Question,ar_Reject,2_Collaborative Completion,no_No Knowledge,h_Hold," \
             "co_Command,qy_Yes-No-question,nd_Dispreferred Answers,j_Joke,bd_Downplayer," \
             "cc_Commitment,ng_Negative Answers,am_Maybe,qrr_Or Clause After Y/N Question,fe_Exclamation,m_Mimic,fa_Apology," \
             "t_About-task,br_Repetition Request,aap_Partial Accept,qh_Rhetorical-Question,tc_Topic Change," \
             "r_Repeat,t1_Self-talk,t3_3rd-party-talk,bh_Rhetorical Question Backchannel,bsc_Partial Reject," \
             "arp_Self-Correct Misspeaking,bs_Summary,f_Follow Me,qr_Or-Question,ft_Thanks," \
             "g_Tag-Question,qo_Open-ended Question,bc_Correct-misspeaking,by_Sympathy,fw_Welcome".split(',')}

out_tags = {'tc': 0, 'h': 1, 'nd': 2, 'qw': 3, 'df': 4, 't1': 5, 'na': 6, 'cs': 7, 'qh': 8, 'by': 9, 'g': 10,
        'ng': 11, 'no': 12, 'bs': 13, 'fe': 14, 'rt': 15, 'd': 16, 't3': 17, 'fa': 18, 'br': 19, 'qrr': 20,
        'arp': 21, 'qr': 22, 'r': 23, 'aap': 24, '2': 25, 'e': 26, 'cc': 27, 'ba': 28, '%': 29, 'b': 30,
        'fw': 31, 'j': 32, 'bk': 33, 'bsc': 34, 's': 35, 'qo': 36, 'co': 37, 'bh': 38, 'aa': 39, 'ft': 40,
        'qy': 41, 'fh': 42, 'm': 43, 'ar': 44, 'f': 45, 'bc': 46, 'bu': 47, 't': 48, 'am': 49, 'fg': 50, 'bd': 51}


class Predictor:

    def __init__(self, model_path, history_len):
        super(Predictor, self).__init__()
        self.has_cuda = torch.cuda.is_available()
        self.out_map = {out_tags[key]:labels_map[key] for key in out_tags}

        self.model = Classifier({'num_layers': 1, 'hidden_dim': 512, 'bidirectional': True, 'embedding_dim': 768,
                            'dropout': 0.1, 'out_dim': len(self.out_map), "sum_emb_rep": False})
        self.model = self.model.to(device)
        self.model.init_weights()
        self.model.load_state_dict(torch.load(model_path, map_location=device))
        self.model.eval()

        self.history_len = history_len
        self.sent = ['<sos>' for _ in range(self.history_len)]
        self.last_speaker = '<None>'

    def predict(self, sentence):
        print(f'inference.predict with ({sentence})')
        curr_spk, snt = sentence.strip().split(':')


        spk = '<same> ' if curr_spk == self.last_speaker else '<switch> '

        self.sent.pop(0)
        self.sent.append(spk + deepcopy(snt[:200]))
        self.last_speaker = curr_spk

        with torch.no_grad():
            output = self.model.forward(self.sent)

        output = torch.nn.functional.softmax(output, dim=1) 
        score, predict = torch.max(output, 1)
        return self.out_map[predict[-1].item()] #we are only interested in the label for last utterance, others only serve as context

    def reset_model(self):
        print('inference.py reset_model')
        self.sent = ['<sos>' for _ in range(self.history_len)]
        self.last_speaker = '<None>'
