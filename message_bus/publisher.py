import paho.mqtt.client as mqtt

# https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php



# non-asynchronous MQTT publisher
class Publisher:

    # TODO pass these in
    host = "localhost"
    port = 1883
    keepalive = 6000
    bind_address = ""

    def __init__(self, message_bus):
        print("Publisher.__init__")
        self.message_bus = message_bus
        self.client = mqtt.Client()
        print("Publisher connecting to Message Bus... ")
        self.client.connect(self.host, self.port, self.keepalive, self.bind_address)
        self.client.loop_start()

    def publish(self, topic, message):
        print("Publisher.publish(" + topic + ", " + message + ")")
        self.client.publish(topic, message)

