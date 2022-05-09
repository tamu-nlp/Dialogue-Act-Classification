import sys
from subscriber import Subscriber
from publisher import Publisher
from heartbeat_publisher import HeartbeatPublisher
from trial_start_handler import TrialStartHandler
from trial_stop_handler import TrialStopHandler
from rollcall_request_handler import RollcallRequestHandler
from asr_handler import AsrHandler
from utils import Utils
from version import Version

# Coordinator class for all things Message Bus
class MessageBus(Utils):

    # shown on startup splash
    name = "TDAC"

    def __init__(self, host, port):
        # init message handlers
        self.message_handlers = [
            AsrHandler(self),
            RollcallRequestHandler(self),
            TrialStartHandler(self),
            TrialStopHandler(self)
        ]

        # connect to the Message Bus
        print(self.name + " is connecting to Message Bus...")
        self.mqtt_url = "tcp://" + host + ":" + str(port)
        self.publisher = Publisher(self, host, port)
        self.subscriber = Subscriber(self, host, port)

    # subscriber has successfully connected to the MQTT broker
    def on_subscriber_connect(self):
        self.heartbeat_publisher = HeartbeatPublisher(self)
        print("Connected to Message Bus at " + self.mqtt_url)
        print(self.name + " version " + Version.version + " running.")
    
    # handle incoming message
    def on_message(self, message_d):
        for handler in self.message_handlers:
            handler.on_message(message_d)

    def publish(self, message_d):
        self.publisher.publish(message_d)
