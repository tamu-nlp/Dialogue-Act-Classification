from common import CommonHeader, CommonMsg
from version import Version
from message import Message
from rollcall_response_message import RollcallResponseMessage

import json

# handle rollcall request message and send response if needed
class RollcallRequestHandler(Message):

    topic = "agent/control/rollcall/request"
    message_type = "agent"
    sub_type = "rollcall:request"

    response = RollcallResponseMessage()

    def __init__(self, message_bus):
        self.message_bus = message_bus

    def on_message(self, message_d):
        if(self.is_subscribed(message_d)):
            self.message_bus.publish(self.response.get_d(message_d))
