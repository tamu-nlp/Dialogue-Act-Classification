from message import Message
from rollcall_response_message import RollcallResponseMessage

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# Handle a rollcall request subscribed from the message bus by publishing
# a rollcall response message.
#

class RollcallRequestMessageHandler(Message):
    topic = 'agent/control/rollcall/request'
    message_type = 'agent'
    sub_type = 'rollcall:request'

    rollcall_response_message = RollcallResponseMessage()

    def on_message(self, message_bus, rollcall_request_d):
        if self.is_subscribed(rollcall_request_d):
            d = self.rollcall_response_message.get_d(
                message_bus,
                rollcall_request_d)
            message_bus.publish(d)
