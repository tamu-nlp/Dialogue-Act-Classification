from common import CommonHeader
from common import CommonMsg
import json

#// published Heartbeat message
#Heartbeat{
#  topic = "agent/uaz_dialog_agent/heartbeats"
#  beat_seconds = 10
#  header{
#    message_type = "status"
#  }
#  msg{
#    sub_type = "heartbeat"
#    source = "uaz_dialog_agent"
#  }
#  data{
#    state = "ok"
#    active = true
#    status = "I am processing messages"
# }
#}

class Heartbeat:
    data = {
        "state" : "ok",
        "active" : True,
        "status" : "I am processing messages"
    }
    header = CommonHeader
    msg = CommonMsg

    def __init__(self, publisher):
        print("Heartbeat.__init__")
        self.publisher = publisher

    def to_json(self, timestamp):
        x = {
            "msg" : self.msg.to_json(timestamp),
            "header" : self.header.to_json(timestamp),
            "data" : self.data
        }
        return json.dumps(x)
