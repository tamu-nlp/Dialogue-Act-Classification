import json
import threading
import time
import logging
from heartbeat_message import HeartbeatMessage
import message_bus

# This class generates a heartbeat message on the heartbeat interval in a
# seperate thread that does not block the MQTT clients 

class HeartbeatPublisher:
    pub_topic = "dialogue_act_classfier/heartbeat"
    heartbeat_seconds = 10 
    hbm = HeartbeatMessage()

    # Create a heartbeat message and send it off for publishing
    def publish_heartbeat(self):
        self.message_bus.publish(self.pub_topic, self.hbm.d)

    # trigger heartbeats on a preset interval
    def pulse(self, foo):
        ticker = threading.Event()
        while not ticker.wait(self.heartbeat_seconds):
            self.publish_heartbeat()

    # Start the pulse in a seperate thread so MQTT clients are not blocked
    def __init__(self, message_bus):
        print("HeartbeatPublisher.__init__")
        self.message_bus = message_bus
        self.publish_heartbeat # send one right away on startup
        worker = threading.Thread(target=self.pulse, args=("foo",))
        worker.start()

    # When a trial starts we must incude the trial_id field from the trial msg
    def on_trial_message(self, trial_message_dict):
        self.hbm = HeartbeatMessage.from_trial_message(trial_message_dict)
        self.publish_heartbeat # send one right away on any trial message
