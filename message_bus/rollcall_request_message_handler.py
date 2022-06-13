from message import Message
from rollcall_response_message import RollcallResponseMessage

# handle rollcall request message and send response if needed
class RollcallRequestMessageHandler(Message):
    topic = "agent/control/rollcall/request"
    message_type = "agent"
    sub_type = "rollcall:request"

    rollcall_response_message = RollcallResponseMessage()

    def on_message(self, message_bus, rollcall_request_message_d):
        if self.is_subscribed(rollcall_request_message_d):
            d = self.rollcall_response_message.get_d(
                rollcall_request_message_d)
            d['data'] = self.rollcall_response_message.get_data()
            message_bus.publish(d)
