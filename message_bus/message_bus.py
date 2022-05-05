from subscriber import Subscriber
from publisher import Publisher
from trial_message import TrialMessage
from heartbeat_publisher import HeartbeatPublisher
import time
import json


# Coordinator class for all things Message Bus
class MessageBus():

    # MQTT client art
    keepalive = 6000

    def __init__(self, host, port):
        print("MessageBus.__init__")
        self.heartbeat_publisher = HeartbeatPublisher(self)
        self.publisher = Publisher(self, host, port, self.keepalive)
        self.subscriber = Subscriber(self, host, port, self.keepalive)

    def on_trial_message(self, trial_message_dict):
        self.heartbeat_publisher.on_trial_message(trial_message_dict)
        trial_sub_type = trial_message_dict["msg"]["sub_type"]
        if(trial_sub_type == "start"):
            # send version info message on trial start
            pass

    def publish(self, topic, message_dict):
        self.publisher.publish(topic, message_dict)
