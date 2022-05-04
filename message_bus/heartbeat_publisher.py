import publisher
import json
import threading
import time
import logging


class HeartbeatPublisher:
    pub_topic = "dialogue_act_classfier/heartbeat"
    heartbeat_interval = 2 # seconds

    def beat(self):
        self.message_bus.publish(self.pub_topic, "Heartbeat message")
        print(time.ctime())

    def __init__(self, message_bus):
        self.message_bus = message_bus
        threading.Timer(self.heartbeat_interval, self.beat).start()
