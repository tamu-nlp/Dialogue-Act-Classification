import json
# Authors:  Joseph Astier, Adarsh Pyarelal

# Define message structures used by multiple Testbed message bus message types

class Version:
    version = "1.0.0"

#  Testbed specification:
#  https://gitlab.asist.aptima.com/asist\
#  /testbed/-/blob/master/MessageSpecs/Common_Header/common_header.json
class CommonHeader:
    d = {
        "timestamp" : "not_set",
        "message_type" : "not_set",
        "version" : "not_set"
    }

    def __init__(self):
        pass

    def set_timestamp(self, timestamp):
        d['timestamp'] = timestamp

    def to_dict(self):
        return self.d
        

#  Testbed specification:
#  https://gitlab.asist.aptima.com/asist\
#  /testbed/-/blob/master/MessageSpecs/Common_Message/common_message.json
class CommonMsg:
    d = {
        "experiment_id" : "not_set",
        "trial_id" : "N/A",
        "timestamp" : "not_set",
        "source" : "not_set",
        "sub_type" : "not_set",
        "version" : Version.version,
        "replay_root_id" : "N/A",
        "replay_id" : "N/A"
    }

    def set_timestamp(self, timestamp):
        d['timestamp'] = timestamp

    def __init__(self):
        pass

    def to_dict(self):
        return self.d
