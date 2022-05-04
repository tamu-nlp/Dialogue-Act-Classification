from publisher import Publisher
import json
import threading
import time
import logging

# This class generates a heartbeat message on the heartbeat interval in a
# seperate thread that does not block the MQTT clients 

class HeartbeatPublisher:
    pub_topic = "dialogue_act_classfier/heartbeat"
    heartbeat_interval = 2 # seconds

    # Create a heartbeat message and send it off for publishing
    def heartbeat(self):
        self.publisher.publish(self.pub_topic, "Heartbeat message")

    # trigger heartbeats on a preset interval
    def pulse(self, foo):
        ticker = threading.Event()
        while not ticker.wait(self.heartbeat_interval):
            self.heartbeat()

    # Start the pulse in a seperate thread so MQTT clients are not blocked
    def __init__(self, publisher):
        print("HeartbeatPublisher.__init__")
        self.publisher = publisher
        self.heartbeat() # send a beat immediately
        t1 = threading.Thread(target=self.pulse, args=("foo",))
        t1.start()

    # Handle a trial message from the Message Bus
    def trial(self, trial_message):
        pass

