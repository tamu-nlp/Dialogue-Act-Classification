from version import Version
from message import Message

class TdacMessage(Message):
    topic = "agent/dialogue_act_classifier/"
    message_type = "agent"
    sub_type = "tdac"
    source = "uaz_tdac_agent"
    data = {
        "label" : "not_set",
        "asr_msg_id" : "not_set"
    }
