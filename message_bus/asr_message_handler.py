from message import Message
from tdac_message import TdacMessage

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# Handle an ASR message subscribed from the Message Bus by publishing
# a TDAC Message based on the ASR message text
#

class AsrMessageHandler(Message):
    topic = 'agent/asr/final'
    message_type = 'observation'
    sub_type = 'asr:transcription'

    tdac_message = TdacMessage()

    # publish a TDAC dictionary based on the ASR dictionary
    def on_message(self, message_bus, asr_d):
        if(self.is_subscribed(asr_d)):
            participant_id = asr_d['data']['participant_id']
            text = asr_d['data']['text']
            utterance = f'{participant_id} : {text}'
            tdac_d = self.tdac_message.get_d(message_bus, utterance, asr_d)
            
            # add asr-only field
            tdac_d['data']['asr_msg_id'] = asr_d['data']['id']

            message_bus.publish(tdac_d)
