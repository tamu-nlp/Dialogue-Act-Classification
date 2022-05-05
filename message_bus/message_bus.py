from subscriber import Subscriber
from publisher import Publisher
from trial_message import TrialMessage
import time
import json


# Coordinator class for all things Message Bus
class MessageBus():

    # MQTT client art
    keepalive = 6000

    def __init__(self, host, port):
        print("MessageBus.__init__")
        self.publisher = Publisher(self, host, port, self.keepalive)
        self.subscriber = Subscriber(self, host, port, self.keepalive)
