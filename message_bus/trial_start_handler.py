from message import Message
from version_info_message import VersionInfoMessage
from heartbeat_message import HeartbeatMessage

# handle trial_start message
class TrialStartHandler(Message):
    topic = "trial"
    message_type = "trial"
    sub_type = "start"

    version_message = VersionInfoMessage()
    heartbeat_message = HeartbeatMessage()

    def __init__(self, message_bus):
        self.message_bus = message_bus

    def on_message(self, message_d):
        if(self.is_subscribed(message_d)):
            self.message_bus.publish(self.version_message.get_d(message_d))
            self.message_bus.publish(self.heartbeat_message.get_d(message_d))

            self.message_bus.heartbeat_publisher.set_trial_message(message_d)
