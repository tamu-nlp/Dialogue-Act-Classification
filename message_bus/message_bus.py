from subscriber import Subscriber
from publisher import Publisher
from heartbeat_publisher import HeartbeatPublisher
from version_info_message import VersionInfoMessage
from trial_start_message_handler import TrialStartMessageHandler
from trial_stop_message_handler import TrialStopMessageHandler
from rollcall_request_message_handler import RollcallRequestMessageHandler
import time
import json
from utils import Utils
from version import Version

# Coordinator class for all things Message Bus
class MessageBus(Utils):

    # shown on startup splash
    name = "TDAC"

    # messages handled
    message_count = 0

    def __init__(self, host, port):
        # init message handlers
        self.rollcall_request_message_handler = \
            RollcallRequestMessageHandler(self)
        self.trial_start_message_handler = \
            TrialStartMessageHandler(self)
        self.trial_stop_message_handler = \
            TrialStopMessageHandler(self)

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
        self.rollcall_request_message_handler.on_message(message_d)
        self.trial_start_message_handler.on_message(message_d)
        self.trial_stop_message_handler.on_message(message_d)

    def publish(self, message_d):
        self.publisher.publish(message_d)
