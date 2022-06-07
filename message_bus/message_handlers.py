from message import Message
from tdac_message import TdacMessage
from rollcall_response_message import RollcallResponseMessage

# Create a classification message based on the ASR message text
class AsrMessageHandler(Message):
    topic = "agent/asr/final"
    message_type = "observation"
    sub_type = "asr:transcription"

    tdac_message = TdacMessage()

    def __init__(self, message_bus):
        self.message_bus = message_bus

    def on_message(self, asr_message_d):
        if(self.is_subscribed(asr_message_d)
        and 'data' in asr_message_d):
            data = asr_message_d['data']
            if ('participant_id' in data
            and 'text' in data):
                part_id = data['participant_id']
                text = data['text']
                label = self.message_bus.classify_utterance(part_id, text)
                tdac_message_d = self.tdac_message.get_d(asr_message_d)
                tdac_message_d['data']['label'] = label
                tdac_message_d['data']['asr_msg_id'] = data['id']
                self.message_bus.publish(tdac_message_d)

# handle rollcall request message and send response if needed
class RollcallRequestMessageHandler(Message):
    topic = "agent/control/rollcall/request"
    message_type = "agent"
    sub_type = "rollcall:request"

    response = RollcallResponseMessage()

    def __init__(self, message_bus):
        self.message_bus = message_bus

    def on_message(self, message_d):
        if(self.is_subscribed(message_d)):
            self.message_bus.publish(self.response.get_d(message_d))

# handle trial_start message
class TrialStartMessageHandler(Message):
    topic = "trial"
    message_type = "trial"
    sub_type = "start"

    def __init__(self, message_bus):
        self.message_bus = message_bus

    def on_message(self, message_d):
        if(self.is_subscribed(message_d)):
            self.message_bus.reset_model()
            self.message_bus.heartbeat_publisher.trial_start(message_d)

# handle trial stop message
class TrialStopMessageHandler(Message):
    topic = "trial"
    message_type = "trial"
    sub_type = "stop"

    def __init__(self, message_bus):
        self.message_bus = message_bus

    def on_message(self, message_d):
        if(self.is_subscribed(message_d)):
            self.message_bus.reset_model()
            self.message_bus.heartbeat_publisher.trial_stop(message_d)
