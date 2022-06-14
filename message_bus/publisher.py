import paho.mqtt.client as mqtt
import json
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
        print(f'Publisher host: {host}, port: {port}')
        keepalive_s = 6000  
        self.message_bus = message_bus
        self.client = mqtt.Client()
        self.client.connect(host, port, keepalive_s, "")
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
