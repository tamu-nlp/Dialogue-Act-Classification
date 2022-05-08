from version import Version
from message import Message

class RollcallResponseMessage(Message):
    topic = "agent/control/rollcall/response"
    message_type = "agent"
    sub_type = "rollcall:response"
    source = "uaz_tdac_agent"
    data = {
        "status": "up"
    }
