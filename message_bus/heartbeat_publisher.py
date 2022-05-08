import json
import threading
import time
import logging
from heartbeat_message import HeartbeatMessage
import message_bus

# This class generates a heartbeat message on the heartbeat interval in a
# seperate thread that does not block the MQTT clients 

class HeartbeatPublisher:
    heartbeat_interval_seconds = 10 # set > 0 to for regular heartbeats
    heartbeat_message = HeartbeatMessage()
    d = heartbeat_message.get_default_d()

    # Create a heartbeat message and send it off for publishing
    def publish_heartbeat(self):
        self.message_bus.publish(self.d)

    # trigger heartbeats on a preset interval
    def pulse(self, phony):
        ticker = threading.Event()
        while not ticker.wait(self.heartbeat_interval_seconds):
            self.publish_heartbeat()

    # Start the pulse in a seperate thread so MQTT clients are not blocked
    def __init__(self, message_bus):
        self.message_bus = message_bus
        splash_msg = (
            "Heartbeat publication interval: " 
            + str(self.heartbeat_interval_seconds)
            + " seconds"
        )
        if(self.heartbeat_interval_seconds > 0):
            # send a heartbeat now
            self.publish_heartbeat()
            # then send them on the heartbeat interval
            print(splash_msg)
            worker = threading.Thread(target=self.pulse, args=("phony",))
            worker.start()
        else:
            print(splash_msg + " (Scheduled heartbeats suppressed)")

    # When a trial starts we must incude the trial_id field from the trial msg
    def set_trial_message(self, message_d):
        self.d = heartbeat_message.get_d(message_d)
        # send one right away on any trial message
        self.publish_heartbeat()
