from message import Message

# handle trial_start message
class TrialStartMessageHandler(Message):
    topic = "trial"
    message_type = "trial"
    sub_type = "start"

    def __init__(self, message_bus):
        self.message_bus = message_bus
        self.test['topic'] = 'trial'
        self.test['msg']['sub_type'] = 'start'
        self.test['header']['message_type'] = 'trial'

    def on_message(self, message_d):
        if(self.is_subscribed(message_d)):
            self.message_bus.reset_model()
            version_message = VersionInfoMessage(self.message_bus)
            self.message_bus.publish(version_message.get_d(message_d))
            message_bus.heartbeat_publisher.start(message_d)

