import publisher
from heartbeat import Heartbeat
import json


class HeartbeatProducer:

    def __init__(self, message_bus):
        print("HeartbeatProducer.__init__")
        self.message_bus = message_bus
        self.heartbeat = Heartbeat
        timestamp = "TIMESTAMP"
        print (self.heartbeat.to_json(self.heartbeat, timestamp))


