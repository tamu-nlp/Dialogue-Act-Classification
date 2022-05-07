from version import Version
from utils import Utils

class RollcallResponseMessage(Utils):
    topic = "agent/control/rollcall/response"
    message_type = "agent"
    sub_type = "rollcall:response"

    data = {
        "status": "up"
    }

    def from_message(self, message_d):
        d = {
            "topic" : self.topic,
            "data" : self.data,
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
