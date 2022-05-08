from utils import Utils

import json

# handle trial stop message
class TrialStopHandler(Utils):
    topic = "trial"
    message_type = "trial"
    sub_type = "stop"

    def __init__(self, message_bus):
        self.message_bus = message_bus

    def on_message(self, message_d):
        if(self.is_subscribed(
                message_d,
                self.topic, self.message_type, self.sub_type)):
            self.message_bus.heartbeat_publisher.on_trial_stop(message_d)
