from message import Message

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# This message is written to the Message Bus whenever we receive an ASR message
#
# Specification: https://github.com/tamu-nlp/Dialogue-Act-Classification/blob/main/message_specs/tdac_message.md
#

class TdacMessage(Message):
    topic = 'agent/dialog_act_classifier'
    message_type = 'agent'
    sub_type = 'dialog_act_label'

    # create a publication dictionary based on the asr dictionary
    def get_d(self, message_bus, asr_d):
        participant_id = asr_d['data']['participant_id']
        utterance = asr_d['data']['text']
        label = message_bus.classify_utterance(participant_id, utterance)

        d = self.get_base_d(asr_d)
        d['data'] = {
            'label' : label,
            'asr_msg_id' : asr_d['data']['id']
        }

        return d
