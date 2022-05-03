import paho.mqtt.client as mqtt

# https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php


class Publisher:
    def __init__(self):
        print("Publisher.__init__")
        self.publisher_client = PublisherClient(self)

    def publish(self, topic, message):
        self.publisher_client.publish(topic, message)


# non-asynchronous MQTT publisher
class PublisherClient:

    # TODO pass these in
    host = "localhost"
    port = 1883
    keepalive = 6000
    bind_address = ""

    client: mqtt.Client

    def __init__(self, publisher):
        print("PublisherClient.__init__")
        self.publisher = publisher
        self.client = mqtt.Client()
        print("Publisher connecting to Message Bus... ")
        self.client.connect(self.host, self.port, self.keepalive, self.bind_address)
        self.client.loop_start()

    def publish(self, topic, message):
        print("PublisherClient.publish(" + topic + ", " + message + ")")
        self.client.publish(topic, message)

