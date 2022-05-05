from common import CommonHeader
import json


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


class VersionInfoMessage (utils.Utils):
    d = {
        "data" : {
            "agent_name": "uaz_tdac_agent",
            "owner" : "University of Arizona",
            "subscribes" : [
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
                }
            ],
            "publishes" : [
                {      
                    "topic": "agent/tdac",
                    "message_type": "event",
                    "sub_type": "Event:dialogue_event"
                },
                {      
                    "topic": "agent/tdac/versioninfo"
                    "message_type": "agent",
                    "sub_type": "versioninfo"
                },
                {      
                    "topic": "agent/tdac/versioninfo"
                    "message_type": "agent",
                    "sub_type": "versioninfo"
                }
            ]
        },
        "header" : {
            "message_type" : "status",
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


    def on_trial_message(self, trial_message_dict):
        # set up the header
        header = CommonHeader.copy(trial_message_dict["header"])

        # set up the msg
        msg = CommonMsg.copy(trial_message_dict["msg"])
        msg["sub_type"] = "versioninfo"
        msg["source"] = "uaz_tdac_agent"

