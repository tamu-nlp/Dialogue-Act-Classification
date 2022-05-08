from message import Message

# handle trial_start message
class TrialStartHandler(Message):
    topic = "trial"
    message_type = "trial"
    sub_type = "start"

    def __init__(self, message_bus):
        self.message_bus = message_bus

    def on_message(self, message_d):
        if(self.is_subscribed(message_d)):
            self.message_bus.heartbeat_publisher.trial_start(message_d)
