from subscriber import Subscriber
from publisher import Publisher
from heartbeat_publisher import HeartbeatPublisher
from version_info_message import VersionInfoMessage
from rollcall_response_message import RollcallResponseMessage
from rollcall_request_message import RollcallRequestMessage
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
        self.rollcall_request_message = RollcallRequestMessage(self)

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

    
    def foo(self, message_d):
        self.rollcall_request_message.on_message(message_d)

    # send message to handler
    def dispatch_message(self, topic, message_d):
        self.message_count += 1
        preamble = "Message " + str(self.message_count) + ": "
        if(topic == "trial"):
            trial_sub_type = message_d["msg"]["sub_type"]
            if(trial_sub_type == "start"):
                print(preamble + "trial [start]")
                self.heartbeat_publisher.on_trial_message(message_d)
                version_info_msg = VersionInfoMessage(message_d)
                self.publish(version_info_msg.topic, version_info_msg.d)
            elif(trial_sub_type == "stop"):
                print(preamble + "trial [stop]")
                self.heartbeat_publisher.on_trial_message(message_d)
        elif(topic == "agent/asr/final"):
            print(preamble + topic)

    def publish(self, topic, message_d):
        self.publisher.publish(topic, message_d)
