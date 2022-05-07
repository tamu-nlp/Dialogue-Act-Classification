import paho.mqtt.client as mqtt
import json
from utils import Utils
from version_info_message import VersionInfoMessage

# https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php

# non-asynchronous Message Bus publisher
class Publisher(Utils):

    def __init__(self, message_bus, host, port):
        self.message_bus = message_bus
        self.client = mqtt.Client()
        self.client.connect(host, port, 6000, "")
        for topic in self.topics(VersionInfoMessage.data["publishes"]):
            print("Publishing on: " + topic)
        self.client.loop_start()

    def publish(self, d):
        # do not publish the topic
        topic = d["topic"]
        del d["topic"] 

        # set timestamps
        ts = self.timestamp()
        d["header"].update({"timestamp": ts})
        d["msg"].update({"timestamp": ts})

        # ship it
        self.client.publish(topic, json.dumps(d))

        # set booleans for realtime publication logging
        if(True):
            print("Published: " + topic)
            if(True):
                print(json.dumps(d, indent=2))
