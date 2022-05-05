from subscriber import Subscriber
from publisher import Publisher
from heartbeat_publisher import HeartbeatPublisher
from version_info_message import VersionInfoMessage
import time
import json

# Coordinator class for all things Message Bus
class MessageBus():

    def __init__(self, host, port):
        print("MessageBus.__init__")
        self.publisher = Publisher(self, host, port)
        self.heartbeat_publisher = HeartbeatPublisher(self)
        # blocking call 
        self.subscriber = Subscriber(self, host, port)

    def on_message(self, topic, message_d):
        if(topic == "trial"):
            self.heartbeat_publisher.on_trial_message(message_d)
            trial_sub_type = message_d["msg"]["sub_type"]
            if(trial_sub_type == "start"):
                version_info_msg = VersionInfoMessage(message_d)
                self.publish(version_info_msg.topic, version_info_msg.d)
        elif(topic == "agent/control/rollcall/request"):
            pass
        elif(topic == "agent/asr/final"):
            pass

    def publish(self, topic, message_d):
        self.publisher.publish(topic, message_d)
