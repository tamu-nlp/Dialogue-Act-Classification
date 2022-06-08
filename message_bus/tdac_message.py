from version import Version
from message import Message

class TdacMessage(Message):
    topic = "agent/dialog_act_classifier/"
    message_type = "agent"
    sub_type = "dialog_act_label"
    source = "dialog_act_classifier"
    data = {
        "label" : "not_set",
        "asr_msg_id" : "not_set"
    }
