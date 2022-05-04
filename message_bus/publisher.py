import paho.mqtt.client as mqtt

# https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php


# non-asynchronous Message Bus publisher
class Publisher:

    def __init__(self, message_bus, host, port, keepalive):
        print("Publisher.__init__")
        self.message_bus = message_bus
        self.client = mqtt.Client()
        self.client.connect(host, port, keepalive, "")
        print("Publisher connected to Message Bus. ")
        self.client.loop_start()

    def publish(self, topic, message):
        print("Publisher.publish(" + topic + ", " + message + ")")
        self.client.publish(topic, message)

