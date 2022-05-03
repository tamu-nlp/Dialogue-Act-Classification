import paho.mqtt.client as mqtt
import json

# https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php


class Subscriber:

    def __init__(self, message_bus):
        print("Subscriber.__init__")
        self.message_bus = message_bus
        self.subscriber_client = SubscriberClient(self)
        self.subscriber_client.startup()

    def do_something_useful(self, client):
        print("do_something_useful")

# Constantly looping MQTT client
class SubscriberClient:

    # TODO pass these in
    host = "localhost"
    port = 1883
    keepalive = 60
    bind_address = ""

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    def on_connect(client, userdata, flags, rc):

        # Paho return code definitions
        if(rc == 0):
            print("Connection successful")
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


    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print("Message from " + msg.topic + ": " + str(msg.payload))

    def __init__(self, subscriber):
        print("SubscriberClient.__init__")
        self.subscriber = subscriber

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    def startup(self):
        print("SubscriberClient.startup.  Connecting to Message Bus... ")
        self.client.connect(self.host, self.port, self.keepalive)
        self.client.loop_forever()

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
