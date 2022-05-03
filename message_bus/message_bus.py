import subscriber
import publisher
from heartbeat_producer import HeartbeatProducer
import time


# This class manages input and output on the message bus
class MessageBus():


    def __init__(self, dac_server):
        print("MessageBus.__init__")
        self.heartbeat_producer = HeartbeatProducer(self)
        self.dac_server = dac_server
        self.publisher = publisher.Publisher()
        self.subscriber = subscriber.Subscriber(self)
        print("MessageBus.__init__ completed")


