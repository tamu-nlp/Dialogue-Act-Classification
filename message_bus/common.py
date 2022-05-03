import json
# Authors:  Joseph Astier, Adarsh Pyarelal

# Define message structures used by multiple Testbed message bus message types

class Version:
    version = "1.0.0"

#  Testbed specification:
#  https://gitlab.asist.aptima.com/asist\
#  /testbed/-/blob/master/MessageSpecs/Common_Header/common_header.json
class CommonHeader:

    def __init__(self):
        print("CommonHeader.__init__")

    def to_json(timestamp):
        x = {
            "timestamp" : timestamp,
            "message_type" : "agent",
            "version" : "from incoming CommonHeader"
        }
        return x
        

#  Testbed specification:
#  https://gitlab.asist.aptima.com/asist\
#  /testbed/-/blob/master/MessageSpecs/Common_Message/common_message.json
class CommonMsg:

    def __init__(self):
        self.experiment_id = "not_set",
        self.trial_id = "N/A",
        self.timestamp = "not_set",
        self.source = "not_set",
        self.sub_type = "not_set",
        self.version = "not_set",
        self.replay_root_id = "N/A",
        self.replay_id = "N/A"

    def to_json(timestamp):
        x = {
            "experiment_id" : "from incoming CommonMsg",
            "trial_id" : "from incoming CommonMsg",
            "timestamp" : timestamp,
            "source" : "uaz_tdac_agent",
            "sub_type" : "heartbeat",
            "version" : Version.version
        }
        return x
