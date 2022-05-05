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
    d = {
        "header" : CommonHeader.d,
        "msg" : CommonMsg.d,
        "data" : {
            "state" : "ok",
            "active" : True,
            "status" : "I am processing messages"
        }
    }

    def from_trial_message(self, trial_message_dict):
        print("HeartbeatMessage.from_trial_message")
        sub_type = trial_msg['msg']['sub_type']
        if(sub_type == 'start'):
            print("Trial start")
        elif f(sub_type == 'stop'):
            print("Trial stop")


#    def set_timestamp(self, timestamp):



#    def to_dict(self, timestamp):
#        msg_dict = self.msg.to_dict()
#        header_dict = self.header.to_dict()

#        msg_dict['timestamp']= timestamp
#        header_dict['timestamp']= timestamp

#        d = {
#            "msg" : msg_dict
#            "header" : header_dict
#            "data" : self.data
#        }
#        return d
