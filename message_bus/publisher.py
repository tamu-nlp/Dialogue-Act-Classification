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
    keepalive = 60
    bind_address = ""

    def __init__(self, publisher):
        print("PublisherClient.__init__")
        self.publisher = publisher

    def publish(self, topic, message):
        print("PublisherClient.publish(" + topic + ", " + message + ")")


    client = mqtt.Client()

    print("Publisher connecting to Message Bus... ")
    client.connect(host, port, keepalive, bind_address)
    client.loop_start()
