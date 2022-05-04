import subscriber
import publisher
from heartbeat_publisher import HeartbeatPublisher
import time


# This class manages input and output on the message bus
class MessageBus():

    def publish(self, topic, payload):
        print("MessageBus publish")
        print("  " + topic)
        print("  " + payload)

    def __init__(self):
        print("MessageBus.__init__")
        self.heartbeat_publisher = HeartbeatPublisher(self)
        self.publisher = publisher.Publisher()
        self.subscriber = subscriber.Subscriber(self)
        print("MessageBus.__init__ completed")


