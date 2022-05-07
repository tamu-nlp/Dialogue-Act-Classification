from utils import Utils
from version_info_message import VersionInfoMessage

import json

# handle trial_start message
class TrialStartMessageHandler(Utils):
    topic = "trial"
    message_type = "trial"
    sub_type = "start"

    version_info_msg = VersionInfoMessage()

    def __init__(self, message_bus):
        self.message_bus = message_bus

    def on_message(self, message_d):
        if(self.is_subscribed(
                message_d,
                self.topic, self.message_type, self.sub_type)):
            self.message_bus.heartbeat_publisher.on_message(message_d)
            self.message_bus.publish(
                    self.version_info_msg.on_message(message_d))

