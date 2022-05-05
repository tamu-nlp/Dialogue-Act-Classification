import json
from utils import Utils
from version import Version 


##// published Version Info message
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
    topic = "agent/tomcat_textAnalyzer/versioninfo"
    d = {
        "data": {
            "agent_name": "uaz_dialog_agent",
            "config": [],
            "dependencies": [],
            "owner": "University of Arizona",
            "publishes": [
                {
                    "message_type": "event",
                    "sub_type": "Event:dialogue_event",
                    "topic": "agent/dialog"
                },
                {
                    "message_type": "agent",
                    "sub_type": "versioninfo",
                    "topic": "agent/tomcat_textAnalyzer/versioninfo"
                },
                {
                    "message_type": "status",
                    "sub_type": "heartbeat",
                    "topic": "agent/uaz_dialog_agent/heartbeats"
                }
            ],
            "source": [
                "https://gitlab.asist.aptima.com:5050/asist/testbed/uaz_dialog_agent:4.1.4"
            ],
            "subscribes": [
                {
                    "message_type": "trial",
                    "sub_type": "start",
                    "topic": "trial"
                },
                {
                    "message_type": "trial",
                    "sub_type": "stop",
                    "topic": "trial"
                },
                {
                    "message_type": "observation",
                    "sub_type": "asr:transcription",
                    "topic": "agent/asr/final"
                },
                {
                    "message_type": "chat",
                    "sub_type": "Event:Chat",
                    "topic": "minecraft/chat"
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
