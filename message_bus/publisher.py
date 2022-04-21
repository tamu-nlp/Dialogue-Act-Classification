import paho.mqtt.client as mqtt
import heartbeat_message

# https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php


class Publisher:
    def __init__(self):
        print("Publisher.__init__")
        self.publisher_client = PublisherClient(self)
#        self.heartbeat_message = heartbeat_message.HeartbeatMessage


# non-asynchronous MQTT publisher
class PublisherClient:

    # TODO pass these in
    host = "localhost"
    port = 1883
    keepalive = 60
    bind_address = ""

    def __init__(self, publisher):
        print("PublisherClient.__init__")
        self.publisher = publisher


    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    client = mqtt.Client()

    print("Publisher connecting to Message Bus... ")
    client.connect(host, port, keepalive, bind_address)
    client.loop_start()

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
