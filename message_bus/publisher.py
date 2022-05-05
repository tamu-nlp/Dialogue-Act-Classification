import paho.mqtt.client as mqtt
from heartbeat_publisher import HeartbeatPublisher
import json
from utils import Utils
import datetime

# https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php

# non-asynchronous Message Bus publisher
class Publisher(Utils):

    def __init__(self, message_bus, host, port):
        print("Publisher.__init__")
        self.message_bus = message_bus
        self.client = mqtt.Client()
        self.client.connect(host, port, 6000, "")
        print("Publisher connected to Message Bus. ")
        self.client.loop_start()

    # add utc timestamps to common header and common msg
    def set_timestamp(self, d):
        timestamp = str(datetime.datetime.utcnow())
        d["header"]["timestamp"] = timestamp
        d["msg"]["timestamp"] = timestamp

    def publish(self, topic, d):

        # set timestamps on all published messages
        self.set_timestamp(d)

        print("Publisher.publish")
        print("  topic : " + topic)
        print("  message : " + json.dumps(d, indent=2))
        self.client.publish(topic, json.dumps(d))

