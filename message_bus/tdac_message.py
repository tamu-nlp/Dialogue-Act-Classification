from message import Message

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# Produced whenever we get an ASR message, uses the DAC 
#

class TdacMessage(Message):
    topic = 'agent/dialog_act_classifier'
    message_type = 'agent'
    sub_type = 'dialog_act_label'

    def get_data(self, message_bus, asr_message_d):

        participant_id = asr_message_d['data']['participant_id']
        text = asr_message_d['data']['text']
        label = message_bus.classify_utterance(participant_id, text)

        return {
            'label' : message_bus.classify_utterance(participant_id, text),
            'asr_msg_id' : asr_message_d['data']['id']
        }
