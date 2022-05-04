import json
from publisher import Publisher
from tdac_message import TdacMessage

# This class generates a heartbeat message on the heartbeat interval in a
# seperate thread that does not block the MQTT clients 

class TdacPublisher:
    pub_topic = "agent/tdac"

    # create a tdac message based on the input
    def on_asr_message(self, asr_msg_dict):
        print("TdacPublisher.on_asr_message")
        # create TDAC message based on ASR
        # publish it
        

    # Keep a ref to the publisher
    def __init__(self, publisher):
        print("TdacPublisher.__init__")
        self.publisher = publisher

