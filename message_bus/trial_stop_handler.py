from message import Message

# handle trial stop message
class TrialStopHandler(Message):
    topic = "trial"
    message_type = "trial"
    sub_type = "stop"

    def __init__(self, message_bus):
        self.message_bus = message_bus

    def on_message(self, message_d):
        if(self.is_subscribed(message_d)):
            self.message_bus.heartbeat_publisher.trial_stop(message_d)
