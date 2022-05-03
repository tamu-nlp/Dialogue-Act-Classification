from common import CommonHeader
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
    pub_topic = "dialogue_act_classfier/heartbeat"

    def message():
        return "tdac_heartbeat_message"

    def __init__(self, publisher):
        self.publisher = publisher
        print("Heartbeat.__init__")

#        while(True):
#            print("timed loop")
#            self.publisher.publish("heartbeat", "The beat goes on")
#            time.sleep(1)
