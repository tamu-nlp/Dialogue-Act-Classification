import paho.mqtt.client as mqtt
import json
from version import Version
from utils import Utils
from version_info_message import VersionInfoMessage

# https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php

class Subscriber(Utils):

    # messages handled
    message_count = 0

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    def on_connect(self, client, userdata, flags, rc):

        # Paho return code definitions
        if(rc == 0):
            for topic in self.topics(VersionInfoMessage.data["subscribes"]):
                self.client.subscribe(topic)
                print("Subscribed to: " + topic)
            self.message_bus.on_subscriber_connect()
        elif(rc == 1):
            print("Connection refused - incorrect protocol version")
        elif(rc == 2):
            print("Connection refused - invalid client identifier")
        elif(rc == 3):
            print("Connection refused - server unavailable")
        elif(rc == 4):
            print("Connection refused - bad username or password")
        elif(rc == 5):
            print("Connection refused - not authorised")
        else:
            print("Connection refused - return code " + str(rc))

    # The callback when a message arrives on a subscribed topic
    def on_message(self, client, userdata, msg):
        # clean payload of extra characters
        payload = str(msg.payload.decode("utf-8"))
        l_brace = payload.find("{")
        r_brace = payload.rfind("}")+1

        # create json message dictionary and add topic
        serialized_json = payload[l_brace : r_brace] 
        message_d = json.loads(serialized_json)
        message_d.update({"topic": msg.topic})

        # report the traffic
        self.message_count += 1
        print(f'message {self.message_count}: {msg.topic}')

        # send to message_bus coordinator for dispatching
        self.message_bus.on_message(message_d)

    def __init__(self, message_bus, host, port):
        self.message_bus = message_bus
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(host, port, 6000)
        self.client.loop_forever()
