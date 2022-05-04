import subscriber
from publisher import Publisher
from heartbeat_publisher import HeartbeatPublisher
from trial_message import TrialMessage
import time


# Coordinator class for all things Message Bus
class MessageBus():

    # MQTT clients
    keepalive = 6000

    def __init__(self, host, port):
        print("MessageBus.__init__")
        self.publisher = Publisher(self, host, port, self.keepalive)
        self.heartbeat_publisher = HeartbeatPublisher(self)
        self.subscriber = subscriber.Subscriber(self, host, port, self.keepalive)
        print("MessageBus.__init__ completed")

    def publish(self, topic, message):
        print("MessageBus publish")
        print("  " + topic)
        print("  " + message)
        self.publisher.publish(topic, message)

    def on_message(self, topic, message):
        print("MessageBus.on_message")
        print("  " + topic)
        print("  " + message)
        if(topic == "trial"):
            trial_message = TrialMessage(message)

