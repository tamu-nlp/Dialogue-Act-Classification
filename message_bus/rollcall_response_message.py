from common import CommonHeader
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


class RollcallResponse:
    topic = "dialogue_act_classfier/heartbeat"
    message_type = "agent"
    sub_type = "rollcall:request"

    def message():
        return "tdac_rollcall_response_message"

