from message import Message
from tdac_message import TdacMessage

# Authors:  Joseph Astier, Adarsh Pyarelal

# Create a classification message based on the ASR message text
class AsrMessageHandler(Message):
    topic = 'agent/asr/final'
    message_type = 'observation'
    sub_type = 'asr:transcription'

    tdac_message = TdacMessage()

    def on_message(self, message_bus, asr_message_d):
        if(self.is_subscribed(asr_message_d)):
            d = self.tdac_message.get_d(asr_message_d)
            d['data'] = self.tdac_message.get_data(message_bus, asr_message_d)
            message_bus.publish(d)
