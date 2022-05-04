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

class HeartbeatMessage:
    data = {
        "state" : "ok",
        "active" : True,
        "status" : "I am processing messages"
    }
    header = CommonHeader
    msg = CommonMsg

    def __init__(self):
        print("Heartbeat.__init__")

    def from_trial_message(self, trial_message_dict):
        print("Heartbeat.from_trial_message")
        sub_type = trial_msg['msg']['sub_type']
        if(sub_type == 'start'):
            print("Trial start")
        elif f(sub_type == 'stop'):
            print("Trial stop")



    def to_dict(self, timestamp):
        d = {
            "msg" : self.msg.to_json(timestamp),
            "header" : self.header.to_json(timestamp),
            "data" : self.data
        }
        return d
