import subscriber
from publisher import Publisher
from heartbeat_publisher import HeartbeatPublisher
from trial_message import TrialMessage
import time
import json


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

    def publish_dict(self, topic, d):
        dump = json.loads(d)
        print("MessageBus publish")
        print("  " + topic)
        print("  " + dump)
        self.publisher.publish(topic, dump)

    def on_trial_message(self, trial_msg):
        self.heartbeat_publisher.on_trial_message(trial_message)


#    def on_message(self, topic, message):
#        print("MessageBus.on_message")
#        print("  " + topic)
#        print("  " + message)
#        if(topic == "trial"):
#            trial_message = TrialMessage(message)

