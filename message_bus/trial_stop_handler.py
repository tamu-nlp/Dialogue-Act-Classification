from message import Message
from heartbeat_message import HeartbeatMessage

# handle trial stop message
class TrialStopHandler(Message):
    topic = "trial"
    message_type = "trial"
    sub_type = "stop"

    heartbeat_message = HeartbeatMessage()

    def __init__(self, message_bus):
        self.message_bus = message_bus

    def on_message(self, message_d):
        if(self.is_subscribed(message_d)):
            self.message_bus.publish(self.heartbeat_message.get_d(message_d))

            self.message_bus.heartbeat_publisher.on_trial_stop(message_d)
