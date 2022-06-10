from message import Message

# Create a classification message based on the ASR message text
class AsrMessageHandler(Message):
    topic = "agent/asr/final"
    message_type = "observation"
    sub_type = "asr:transcription"

    tdac_message = TdacMessage()

    def __init__(self, message_bus):
        self.message_bus = message_bus

    def on_message(self, asr_message_d):
        participant_id = asr_message_d['data']['participant_id']
        text = asr_message_d['data']['text']
        label = self.message_bus.classify_utterance(participant_id, text)
        tdac_message_d = self.tdac_message.get_d(asr_message_d)
        tdac_message_d['data']['label'] = label
        tdac_message_d['data']['asr_msg_id'] = data['id']
        self.message_bus.publish(tdac_message_d)
