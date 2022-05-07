from common import CommonHeader, CommonMsg
from version import Version
from utils import Utils

import json

# published Rollcall response message
#RollcallResponse {
#  topic = "agent/control/rollcall/response"
#  header {
#    message_type = "agent"
#  }
#  msg {
#    sub_type = "rollcall:response"
#    source = "uaz_dialog_agent"
#  }
#  data {
#    status = "up"
#  }
#}
# 
#  subscribed Rollcall request message
# RollcallRequest {
#   topic = "agent/control/rollcall/request"
#   header {
#     message_type = "agent"
#   }
#   msg {
#     sub_type = "rollcall:request"
#   }
# }


# handle rollcall request message and send response if needed
class RollcallRequestMessage(Utils):

    d = {
        "topic": "agent/control/rollcall/request",
        "header" : {
            "message_type" : "agent"
        },
        "msg" : {
            "sub_type": "rollcall:request"
        }
    }

    def __init__(self, message_bus):
        self.message_bus = message_bus

    def on_message(self, message_d):
        if(self.is_subscribed(self.d, message_d)):
            print("RollcallRequestMessage subscribed")
        else:
            print("RollcallRequestMessage not subscribed")


    def from_message(self, message_d):

        # update common header
        src = message_d["header"]
        dst = self.d["header"]
        self.update_field(src, dst, "version")

        # update common msg
        src = message_d["msg"]
        dst = self.d["msg"]
        self.update_field(src, dst, "experiment_id")
        self.update_field(src, dst, "replay_parent_type")
        self.update_field(src, dst, "replay_id")
        self.update_field(src, dst, "replay_parent_id")
        self.update_field(src, dst, "trial_id")
