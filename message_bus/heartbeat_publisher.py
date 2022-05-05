import json
import threading
import time
import logging
from heartbeat_message import HeartbeatMessage
import publisher

# This class generates a heartbeat message on the heartbeat interval in a
# seperate thread that does not block the MQTT clients 

class HeartbeatPublisher:
    pub_topic = "dialogue_act_classfier/heartbeat"
    heartbeat_seconds = 10 
    heartbeat_message = HeartbeatMessage()

    # Create a heartbeat message and send it off for publishing
    def publish_heartbeat(self):
        self.publisher.publish(self.pub_topic, self.heartbeat_message.d)

    # trigger heartbeats on a preset interval
    def pulse(self, foo):
        ticker = threading.Event()
        while not ticker.wait(self.heartbeat_seconds):
            self.publish_heartbeat()

    # Start the pulse in a seperate thread so MQTT clients are not blocked
    def __init__(self, publisher):
        print("HeartbeatPublisher.__init__")
        self.publisher = publisher
        worker = threading.Thread(target=self.pulse, args=("foo",))
        worker.start()

    # Handle a trial message from the Message Bus
    def on_trial_message(self, trial_message_dict):
        self.heartbeat_message=Heartbeat.from_trial_message(trial_message_dict)
