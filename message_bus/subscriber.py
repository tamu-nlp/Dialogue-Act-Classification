import paho.mqtt.client as mqtt
import json
from version import Version
from trial_message_handler import *
from rollcall_request_message_handler import RollcallRequestMessageHandler
from asr_message_handler import AsrMessageHandler
from chat_message_handler import ChatMessageHandler

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# Blocking MQTT client
#
# https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php
#

class Subscriber():

    # messages handled
    message_count = 0

    # every relevant message gets a handler
    message_handlers = (
        AsrMessageHandler(),
        ChatMessageHandler(),
        RollcallRequestMessageHandler(),
        TrialStartMessageHandler(),
        TrialStopMessageHandler()
    )

    def subscribe(self, topic):
        self.client.subscribe(topic)
        print(f'Subscribed to: {topic}')

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    def on_connect(self, client, userdata, flags, rc):

        # Paho return code definitions
        if(rc == 0):
            self.subscribe(AsrMessageHandler.topic)
            self.subscribe(RollcallRequestMessageHandler.topic)
            self.subscribe(TrialMessageHandler.topic)
            if not self.nochat:
                self.subscribe(ChatMessageHandler.topic)
            self.message_bus.on_subscriber_connect()
        elif(rc == 1):
            print('Connection refused - incorrect protocol version')
        elif(rc == 2):
            print('Connection refused - invalid client identifier')
        elif(rc == 3):
            print('Connection refused - server unavailable')
        elif(rc == 4):
            print('Connection refused - bad username or password')
        elif(rc == 5):
            print('Connection refused - not authorised')
        else:
            print('Connection refused - return code ' + str(rc))

    # The callback when a message arrives on a subscribed topic
    def on_message(self, client, userdata, msg):
        # clean payload of extra characters
        payload = str(msg.payload.decode('utf-8'))
        l_brace = payload.find('{')
        r_brace = payload.rfind('}')+1

        # create json message dictionary and add topic
        serialized_json = payload[l_brace : r_brace] 
        message_d = json.loads(serialized_json)
        message_d.update({'topic': msg.topic})

        # report the traffic
        self.message_count += 1
        print(f'message {self.message_count}: {msg.topic}')

        # send message to each handler
        for handler in self.message_handlers:
            handler.on_message(self.message_bus, message_d)

    def __init__(self, message_bus, host, port, nochat):
        mqtt_keepalive = 6000 # seconds
        self.nochat = nochat
        self.message_bus = message_bus
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(host, port, mqtt_keepalive)

        # main loop for this MQTT application
        self.client.loop_forever()
