import json
import threading
import time
import logging
from heartbeat_message import HeartbeatMessage
import message_bus

# This class generates a heartbeat message on the heartbeat interval in a
# seperate thread that does not block the MQTT clients 

class HeartbeatPublisher:
    heartbeat_interval_seconds = 10 
    hbm = HeartbeatMessage()
    d = hbm.d

    # Create a heartbeat message and send it off for publishing
    def publish_heartbeat(self):
        print("HeartbeatPublisher.publish_heartbeat")
        self.message_bus.publish(self.hbm.topic, self.d)

    # Create a heartbeat message and send it off for publishing
    def foo_heartbeat(self):
        print("HeartbeatPublisher.foo_heartbeat")

    # trigger heartbeats on a preset interval
    def pulse(self, phony):
        ticker = threading.Event()
        while not ticker.wait(self.heartbeat_interval_seconds):
            self.publish_heartbeat()

    # Start the pulse in a seperate thread so MQTT clients are not blocked
    def __init__(self, message_bus):
        print("HeartbeatPublisher.__init__(self, message_bus)")
        self.message_bus = message_bus
        # send a heartbeat as soon as possible
        self.publish_heartbeat()
        # then send them on the heartbeat interval
        worker = threading.Thread(target=self.pulse, args=("phony",))
        worker.start()

    # When a trial starts we must incude the trial_id field from the trial msg
    def on_trial_message(self, trial_message_dict):
        print("HeartbeatPublisher.on_trial_message")
        self.d = self.hbm.from_trial_message(trial_message_dict)
        # send one right away on any trial message
        self.publish_heartbeat()
