# Authors:  Joseph Astier, Adarsh Pyarelal

# Define message structures used by multiple Testbed message bus message types

#  Testbed specification:
#  https://gitlab.asist.aptima.com/asist\
#  /testbed/-/blob/master/MessageSpecs/Common_Header/common_header.json
class CommonHeader:

    def __init__(self):
        self.timestamp = 'N/A'
        self.message_type = 'N/A'
        self.version = 'N/A'

    def write_json():
        return "JSON"
        

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

    def write_json():
        return "JSON"
        
