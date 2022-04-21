from common import CommonHeader
import json

class HeartbeatMessage:
    pub_topic = "dialogue_act_classfier/heartbeat"

    def message():
        return "tdac_heartbeat_message"

    def __init__(self):
        print("HeartbeatMessage.__init__")
