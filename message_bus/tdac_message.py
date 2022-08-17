from message import Message

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# This message is written to the Message Bus whenever we receive an ASR message
#
# Specification: https://github.com/tamu-nlp/Dialogue-Act-Classification/blob/main/message_specs/tdac_message.md
#

class TdacMessage(Message):
    topic = 'agent/AC_TAMU_TA1_DialogActClassifier'
    message_type = 'agent'
    sub_type = 'dialog_act_label'

    # create a publication dictionary based on the id and text
    def get_d(self, message_bus, utterance, message_d):
        d = self.get_base_d(message_bus, message_d)
        label = message_bus.classify_utterance(utterance)
        d['data'] = {
            'label' : label
        }
        return d
