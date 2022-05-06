import paho.mqtt.client as mqtt
from heartbeat_publisher import HeartbeatPublisher
import json
from utils import Utils
import datetime
import re

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

    # UTC timezone formatted as ISO 8601: YYYY-MM-DDThh:mm:ss.ssssZ
    def set_timestamp(self, d):
        t = datetime.datetime.utcnow()
        iso = t.isoformat(timespec='microseconds')
        timestamp = str(iso) + 'Z'
        pattern = "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}[.]?[0-9]{0,}?Z"


        d["header"]["timestamp"] = timestamp
        d["msg"]["timestamp"] = timestamp

    def publish(self, topic, d):

        # set timestamps on all published messages
        self.set_timestamp(d)

        print("Publisher.publish")
        print("  topic : " + topic)
        print("  message : " + json.dumps(d, indent=2))
        self.client.publish(topic, json.dumps(d))

