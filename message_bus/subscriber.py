import paho.mqtt.client as mqtt
import json

# https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php

# This class receives messages on subscribed topics and sends them
# to the MessageBus owning class as dictionaries for further processing

# Constantly looping MQTT client
class Subscriber:

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    def on_connect(self, client, userdata, flags, rc):

        # Paho return code definitions
        if(rc == 0):
            print("Subscriber connected to the Message Bus ")
            client.subscribe("trial")
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

    # Get extra characters off the ends of the msg.payload string
    def clean_msg_payload(self, msg):
        payload = str(msg.payload.decode("utf-8"))
        l_brace = payload.find("{")
        r_brace = payload.rfind("}")+1
        clean_payload = payload[l_brace : r_brace] 
        return clean_payload

    def on_trial_message(self, client, userdata, msg):
        clean_json_txt = self.clean_msg_payload(msg)
        trial_message_dict = json.loads(clean_json_txt)
        self.message_bus.on_trial_message(trial_message_dict)

    # The callback when a message arrives on a subscribed topic
    def on_message(self, client, userdata, msg):
        json_string = self.clean_msg_payload(msg)
        self.message_bus.on_message(msg.topic, json_string)

    def __init__(self, message_bus, host, port, keepalive):
        self.message_bus = message_bus
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.message_callback_add("trial",self.on_trial_message)
        self.client.connect(host, port, keepalive)
        self.client.loop_forever()
