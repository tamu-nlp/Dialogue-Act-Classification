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

    # create a publication dictionary based on the id and text
    def get_d(self, message_bus, participant_id, text, message_d):
        label = message_bus.classify_utterance(participant_id, text)

        d = self.get_base_d(message_d)
        d['data'] = {
            'label' : label
        }

        return d
