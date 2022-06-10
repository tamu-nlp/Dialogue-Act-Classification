from message import Message


# handle trial stop message
class TrialStopMessageHandler(Message):
    topic = "trial"
    message_type = "trial"
    sub_type = "stop"

    def __init__(self, message_bus):
        self.message_bus = message_bus
        self.test['topic'] = 'trial'
        self.test['msg']['sub_type'] = 'stop'
        self.test['header']['message_type'] = 'trial'

    def on_message(self, message_d):
        if(self.is_subscribed(message_d)):
            self.message_bus.reset_model()
            self.message_bus.heartbeat_publisher.stop(message_d)

