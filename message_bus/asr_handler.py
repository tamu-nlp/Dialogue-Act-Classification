from message import Message
from tdac_message import TdacMessage

# handle ASR message
class AsrHandler(Message):
    topic = "agent/asr/final"
    message_type = "observation"
    sub_type = "asr:transcription"

    tdac_message = TdacMessage()

    def __init__(self, message_bus):
        self.message_bus = message_bus

    def on_message(self, message_d):
        if(self.is_subscribed(message_d)):
            self.message_bus.publish.self.tdac_message.get_d(message_d))
