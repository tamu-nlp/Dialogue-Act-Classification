from common import CommonHeader, CommonMsg
from version import Version
from utils import Utils
from rollcall_response_message import RollcallResponseMessage

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
class RollcallRequestMessageHandler(Utils):

    topic = "agent/control/rollcall/request"
    message_type = "agent"
    sub_type = "rollcall:request"

    def __init__(self, message_bus):
        self.message_bus = message_bus


    def on_message(self, message_d):
        if(self.is_subscribed(
                message_d, 
                self.topic, self.message_type, self.sub_type)):
            response = RollcallResponseMessage()
            self.message_bus.publish(response.from_message(message_d))
