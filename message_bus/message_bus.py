import subscriber
from publisher import Publisher
from heartbeat_publisher import HeartbeatPublisher
import time


# This class manages input and output on the message bus
class MessageBus():

    publisher: Publisher

    def __init__(self):
        print("MessageBus.__init__")
        self.publisher = Publisher(self)
        self.heartbeat_publisher = HeartbeatPublisher(self.publisher)
        self.subscriber = subscriber.Subscriber(self)
        print("MessageBus.__init__ completed")


    def publish(self, topic, message):
        print("MessageBus publish")
        print("  " + topic)
        print("  " + message)
        self.publisher.publish(topic, message)

