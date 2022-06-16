import paho.mqtt.client as mqtt
import json
from version_info_message import VersionInfoMessage
from tdac_message import TdacMessage
from heartbeat_message import HeartbeatMessage
from rollcall_response_message import RollcallResponseMessage

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# Asynchronous Message Bus publisher
#
# https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php
#

class Publisher():

    published_messages = (
        VersionInfoMessage,
        TdacMessage,
        RollcallResponseMessage,
        HeartbeatMessage
    )

    def __init__(self, message_bus, host, port):
        print(f'Publisher host: {host}, port: {port}')
        mqtt_keepalive = 6000 # seconds 
        self.message_bus = message_bus
        self.client = mqtt.Client()
        self.client.connect(host, port, mqtt_keepalive, '')
        for publication in self.published_messages:
            print(f'Publishing on: {publication.topic}')

    def publish(self, d):
        topic = d['topic']

        # Publish only data, msg, and header.
        output_d = {
            'data':d['data'],
            'header': d['header'],
            'msg' : d['msg']
        }
        publication = json.dumps(output_d, separators=(',', ':'))
        self.client.publish(topic, publication)
