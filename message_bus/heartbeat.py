from common import CommonHeader
import json

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
