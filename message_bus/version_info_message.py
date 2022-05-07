import json
from utils import Utils
from version import Version 

from heartbeat_message import HeartbeatMessage

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
    d = {
        "data": {
            "agent_name": "uaz_tdac_agent",
#            "config": [],
#            "dependencies": [],
            "owner": "University of Arizona",
            "publishes": [
                {
                    "topic": "agent/uaz_tdac",
                    "message_type": "event",
                    "sub_type": "Event:tdac_event"
                },
                {
                    "topic": RollcallResponse.topic,
                    "message_type": RollcallResponse.message_type,
                    "sub_type": RollcallResponse.sub_type
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
        },
        "header" : {
            "message_type" : "agent",
            "timestamp" : "not_set",
            "version" : "not_set"
        },
        "msg" : {
            "experiment_id" : "not_set",
            "source" : "uaz_tdac_agent",
            "sub_type": "versioninfo",
            "timestamp" : "not_set",
            "version": Version.version
        }
    }


    def __init__(self, message_d):

        # update common header
        src = message_d["header"]
        dst = self.d["header"]
        self.update_field(src, dst, "version")

        # update common msg
        src = message_d["msg"]
        dst = self.d["msg"]
        self.update_field(src, dst, "experiment_id")
        self.update_field(src, dst, "replay_parent_type")
        self.update_field(src, dst, "replay_id")
        self.update_field(src, dst, "replay_parent_id")
        self.update_field(src, dst, "trial_id")
