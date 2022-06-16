from message import Message
from tdac_message import TdacMessage

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# Handle an ASR message subscribed from the Message Bus by creating
# and publishing a TDAC Message based on the ASR message text
#

class AsrMessageHandler(Message):
    topic = 'agent/asr/final'
    message_type = 'observation'
    sub_type = 'asr:transcription'

    tdac_message = TdacMessage()

    # publish a TDAC dictionary based on the ASR dictionary
    def on_message(self, message_bus, asr_d):
        if(self.is_subscribed(asr_d)):
            d = self.tdac_message.get_d(message_bus, asr_d)
            message_bus.publish(d)
