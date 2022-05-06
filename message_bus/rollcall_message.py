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
    pub_topic = "dialogue_act_classfier/heartbeat"

    def message():
        return "tdac_rollcall_response_message"

    def __init__(self, publisher):
        self.publisher = publisher
        print("Heartbeat.__init__")

#        while(True):
#            print("timed loop")
#            self.publisher.publish("heartbeat", "The beat goes on")
#            time.sleep(1)
