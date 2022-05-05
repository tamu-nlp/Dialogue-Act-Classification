import paho.mqtt.client as mqtt
from heartbeat_publisher import HeartbeatPublisher
import json

# https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php

# non-asynchronous Message Bus publisher
class Publisher:

    def __init__(self, message_bus, host, port):
        print("Publisher.__init__")
        self.message_bus = message_bus
        self.client = mqtt.Client()
        self.client.connect(host, port, 0, "")
        print("Publisher connected to Message Bus. ")
        self.client.loop_start()

    def publish(self, topic, d):
        print("Publisher.publish")
        print("  topic : " + topic)
        print("  message : " + json.dumps(d, indent=2))
        self.client.publish(topic, json.dumps(d))

