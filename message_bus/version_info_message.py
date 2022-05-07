import json
from utils import Utils
from version import Version 

from heartbeat_message import HeartbeatMessage
from rollcall_response_message import RollcallResponseMessage

##// published Version Info message as published by Dialog Agent
#VersionInfo{
#  testbed = "https://gitlab.asist.aptima.com:5050/asist/testbed/uaz_dialog_agent"
#  topic = "agent/tomcat_textAnalyzer/versioninfo"
#  header {
#    message_type = "agent"
#  }
#  msg {
#    sub_type = "versioninfo"
#    source = "uaz_dialog_agent"
#  }
#  data {
#    agent_name = "uaz_dialog_agent"
#    owner = "University of Arizona"
#  }
#}


class VersionInfoMessage (Utils):
    topic = "agent/uaz_tdac/versioninfo"
    message_type = "agent"
    sub_type = "versioninfo"

    data = {
        "agent_name": "uaz_tdac_agent",
        "owner": "University of Arizona",
        "publishes": [
            {
                "topic": "agent/uaz_tdac",
                "message_type": "event",
                "sub_type": "Event:tdac_event"
            },
            {
                "topic": RollcallResponseMessage.topic,
                "message_type": RollcallResponseMessage.message_type,
                "sub_type": RollcallResponseMessage.sub_type
            },
            {
                "topic": topic,
                "message_type": message_type,
                "sub_type": sub_type
            },
            {
                "topic": HeartbeatMessage.topic,
                "message_type":  HeartbeatMessage.message_type,
                "sub_type":  HeartbeatMessage.sub_type
            }
        ],
        "source": [
            "https://gitlab.asist.aptima.com:5050/asist/testbed/"
            + "uaz_tdac_agent:"
            + Version.version
        ],
        "subscribes": [
            {
                "topic": "trial",
                "message_type": "trial",
                "sub_type": "start"
            },
            {
                "topic": "trial",
                "message_type": "trial",
                "sub_type": "stop"
            },
            {
                "topic": "agent/asr/final",
                "message_type": "observation",
                "sub_type": "asr:transcription"
            },
            {
                "topic": "agent/control/rollcall/request",
                "message_type": "agent",
                "sub_type": "rollcall:request"
            }
        ],
        "version": Version.version
    }

    def on_message(self, message_d):
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
