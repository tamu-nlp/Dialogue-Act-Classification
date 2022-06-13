import paho.mqtt.client as mqtt
import json
from utils import Utils
from version_info_message import VersionInfoMessage
from tdac_message import TdacMessage
from heartbeat_message import HeartbeatMessage
from rollcall_response_message import RollcallResponseMessage

# https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php

# non-asynchronous Message Bus publisher
class Publisher():

    published_messages = (
        VersionInfoMessage,
        TdacMessage,
        RollcallResponseMessage,
        HeartbeatMessage
    )

    def __init__(self, message_bus, host, port):
        self.message_bus = message_bus
        self.client = mqtt.Client()
        self.client.connect(host, port, 6000, "")
        for publication in self.published_messages:
            print(f'Publishing on: {publication.topic}')

    def publish(self, d):
        topic = d['topic']

        # do not publish the topic
        published_d = {
            "data":d["data"],
            "header": d["header"],
            "msg" : d["msg"]
        }

        # ship it 
        publication = json.dumps(published_d, separators=(',', ':'))
        self.client.publish(topic, publication)

        # set booleans for realtime publication logging
        if(True):
            print(f"Published on {topic}: ")
        if(True):
            print(publication)
