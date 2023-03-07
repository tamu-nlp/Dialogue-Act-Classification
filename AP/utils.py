import random
import torch
import numpy as np
from copy import deepcopy

#how many predicted Bs were connected with correct A, wrong A, B, None
def get_ap_stats(pred_b_indices, output_ap, ap_out_true, ap_part_out, start_ind):
    #pred_b_indices: a tensor of indices that were considered Bs tensor([ 9, 18, 20])
    #output_ap: a list of size |pred_b_indices|, each ind has matched A or -1,  [7, 17, -1]
    #ap_out_true: actual annotations. A list of lists. For each ind, if its A/None then list is empty. If a B, 
                    #then the correct ind of the As it should be connected to

    ap_part_out = np.array(ap_part_out)
    b_count = np.sum((ap_part_out[start_ind:] == 1)).item() #b_count total numb of actual Bs
    correct_linked = 0
    # correct_none = 0
    # wrong_none = 0 #wrongly connected with a none

    b_indices = torch.tensor(list(range(start_ind, len(ap_part_out)))) 
    b_indices = b_indices[ap_part_out[start_ind:] == 1].tolist() #ind list of actual Bs
    # not_considered_b = len(list(b_indices))

    num_corr_pred_b = 0
    con_wrong_a = 0 #numb of actual Bs connected with a wrong A
    con_b, con_none = 0, 0
    not_connected = 0 #utt classified as a B, but could not be linked with any A using heuristics
    not_considered_b = len(list(set(b_indices))) 
    if pred_b_indices != None:
        for i, b_ind in enumerate(pred_b_indices):
            ap_y = ap_out_true[b_ind] #a list
            if len(ap_y) > 0: #is a B
                num_corr_pred_b+=1
                if output_ap[i] in ap_y: correct_linked+=1
                # elif output_ap[i] == -1: wrong_none+=1
                
                else: #is a B, but not correctly linked
                    if output_ap[i] != -1:
                        true_type = ap_part_out[output_ap[i]] #the actual label of the utt that has been connected with this B
                        if true_type == 0: con_wrong_a+=1
                        elif true_type == 1: con_b+=1
                        else: con_none+=1
                    else: not_connected+=1


        pred_b_indices = pred_b_indices.tolist()
        not_considered_b = len(list(set(b_indices) - set(pred_b_indices)))
    
    return b_count, num_corr_pred_b, correct_linked, not_considered_b, con_wrong_a, con_b, con_none, not_connected
    #b_count: total utts actually Bs
    #num_corr_pred_b: of those predicted, how many were correctly predicted as Bs
    #correct_linked: from the correctly predicted, how many were rightly linked
    #not_considered_b_count: numb of Bs that were not classified as Bs
    #con_wrong_a: Bs connected with wrong A
    #con_b/con_none: Bs connected with a B/none
    #not_connected: -1, the A could not be found


def get_heuristics_linkage(all_ap_preds, data, window_size):
    #all_ap_preds: a list of tensors. Each list is the predicted parts for all utts in a dialogue
    total_b_count, total_num_corr_pred_b, total_correct_linked, total_not_considered_b_count = 0,0,0,0
    total_con_wrong_a, total_con_b, total_con_none, total_not_connected = 0,0,0,0
    for i in range(len(all_ap_preds)):
        ap_preds = all_ap_preds[i]

        b_indices, ap_con_pred = heuristics_linkage_dialogue(ap_preds, data['speaker_list'][i], data['window_ind_tensor'][i].item(), window_size)
        b_count, num_corr_pred_b, correct_linked, not_considered_b_count, con_wrong_a, con_b, con_none, not_connected = \
        get_ap_stats(b_indices, ap_con_pred, data['ap_conn_labels'][i], data['ap_part_labels'][i], data['window_ind_tensor'][i].item())
        total_b_count+=b_count
        total_num_corr_pred_b+=num_corr_pred_b
        total_correct_linked+=correct_linked
        total_not_considered_b_count+=not_considered_b_count
        total_con_wrong_a+=con_wrong_a
        total_con_b+=con_b
        total_con_none+=con_none
        total_not_connected+=not_connected

    return total_b_count, total_num_corr_pred_b, total_correct_linked, total_not_considered_b_count, total_con_wrong_a, total_con_b, total_con_none, total_not_connected


def heuristics_linkage_dialogue(y_part, spk_list, start_index, window_size):
    batch_size = len(spk_list)
    spk_list = np.array(spk_list.cpu())
    part_a_list = y_part.detach().clone() #computational path not needed
    part_a_list = part_a_list == 0
    part_b_list = y_part[start_index:].detach().clone()
    part_b_list = part_b_list == 1

    b_indices = np.array(list(range(start_index, batch_size))) #len(spk_list)

    assert b_indices.shape[0] == part_b_list.size()[0]
    # b_indices = b_indices[part_b_list[start_index:]] #get those indices predicted as B's
    b_indices = b_indices[part_b_list] #get those indices predicted as B's

    if b_indices.size == 0:
        return None, None

    if torch.sum((part_a_list == 1)).item() == batch_size: #all sentences predicted as As
        return None, None #decide returns

    a_indices = np.array(list(range(0, batch_size)))
    a_indices = a_indices[part_a_list]

    ap_out = []
    for b_ind in b_indices:
        curr_spk = spk_list[b_ind]

        #get most recent A that has different spk
        potential_a = deepcopy(a_indices[a_indices < b_ind])
        if potential_a.shape[0] > 0:

            potential_a = potential_a[spk_list[potential_a] != curr_spk] #diff spks
            potential_a = potential_a[b_ind - potential_a <= window_size] #utts falling within window size of curr utts
            ap_out.append(potential_a[-1] if potential_a.size else -1) #if non empty: get most recent A satisfying conds
        #there is no A for this B --> wrongly classified append -1
        else: ap_out.append(-1)
    return torch.tensor(b_indices), ap_out
    #ind number of predicted B utts, their corresponding predicted A ap indices

def set_seed(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
    random.seed(seed)
    np.random.seed(seed)