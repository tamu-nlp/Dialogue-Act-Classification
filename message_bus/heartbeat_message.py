from version import Version
from message import Message

class HeartbeatMessage(Message):
    topic = "agent/dialogue_act_classfier/heartbeat"
    message_type = "status"
    sub_type = "heartbeat"
    source = "uaz_tdac_agent"
    data = {
        "state" : "ok",
        "active" : True,
        "status" : "I am processing messages"
    }
