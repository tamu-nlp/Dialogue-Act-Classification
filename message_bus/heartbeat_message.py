from version import Version
from utils import Utils

class HeartbeatMessage(Utils):
    topic = "agent/dialogue_act_classfier/heartbeat"
    message_type = "status"
    sub_type = "heartbeat"

    # default values
    def no_message(self):
        d = {
            "topic" : self.topic,
            "data" : {
                "state" : "ok",
                "active" : True,
                "status" : "I am processing messages"
            },
            "header" : {
                "message_type" : self.message_type,
                "version" : "not_set"
            },
            "msg" : {
                "source" : "uaz_tdac_agent",
                "sub_type": self.sub_type,
                "version": Version.version
            }
        }

        return d

    # Set dictionary values from trial message dictionary
    def from_message(self, message_d):

        d = {
            "topic" : self.topic,
            "data" : {
                "state" : "ok",
                "active" : True,
                "status" : "I am processing messages"
            },
            "header" : {
                "message_type" : self.message_type,
                "version" : message_d["header"]["version"]
            },
            "msg" : {
                "source" : "uaz_tdac_agent",
                "sub_type": self.sub_type,
                "version": Version.version
            }
        }

        self.update_common_msg(message_d, d)

        return d
