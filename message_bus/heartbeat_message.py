from common import CommonHeader
import json

class HeartbeatMessage:
    pub_topic = "dialogue_act_classfier/heartbeat"

    def message():
        return "tdac_heartbeat_message"

    print("HeartbeatMessage constructed")
