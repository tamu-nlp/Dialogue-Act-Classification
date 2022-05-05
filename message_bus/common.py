import json
import time
# Authors:  Joseph Astier, Adarsh Pyarelal

# Define message structures used by multiple Testbed message bus message types

class Version:
    version = "1.0.0"

# We need a timestamp ala this:   "2022-04-30T22:06:26.305716Z"

#  Testbed specification:
#  https://gitlab.asist.aptima.com/asist\
#  /testbed/-/blob/master/MessageSpecs/Common_Header/common_header.json
class CommonHeader:
    d = {
        "timestamp" : "not_set",     # required field
        "message_type" : "not_set",  # required field
        "version" : "not_set"        # required field
    }

    # every field is required so we can just copy everything
    def copy(self, src):
        for(key, value) in src.items():
            self.d[key] = value


#  Testbed specification:
#  https://gitlab.asist.aptima.com/asist\
#  /testbed/-/blob/master/MessageSpecs/Common_Message/common_message.json
class CommonMsg:

    # CommonMsg struct 
    d = {
        "experiment_id" : "not_set",  
        "trial_id" : "N/A",
        "timestamp" : "not_set",
        "source" : "not_set",
        "sub_type" : "not_set",
        "version" : "not_set",
        "replay_root_id" : "N/A",
        "replay_id" : "N/A"
    }

