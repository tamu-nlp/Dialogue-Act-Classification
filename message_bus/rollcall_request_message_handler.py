from message import Message

# handle rollcall request message and send response if needed
class RollcallRequestMessageHandler(Message):
    topic = "agent/control/rollcall/request"
    message_type = "agent"
    sub_type = "rollcall:request"

    response = RollcallResponseMessage()

    def __init__(self, message_bus):
        self.message_bus = message_bus
        self.test['topic'] = 'trial'
        self.test['msg']['sub_type'] = 'start'
        self.test['header']['message_type'] = 'trial'

    def on_message(self, message_d):
        if(self.is_subscribed(message_d)):
            self.message_bus.publish(self.response.get_d(message_d))

