from message import Message
from tdac_message import TdacMessage
from rollcall_response_message import RollcallResponseMessage

# handle ASR message
class AsrMessageHandler(Message):
    topic = "agent/asr/final"
    message_type = "observation"
    sub_type = "asr:transcription"

    tdac_message = TdacMessage()

    def __init__(self, message_bus):
        self.message_bus = message_bus

    def on_message(self, message_d):
        if(self.is_subscribed(message_d)
        and 'data' in message_d):
            data = message_d['data']
            if ('participant_id' in data
            and 'text' in data):
                label = self.message_bus.classify_utterance(
                data['participant_id'], data['text'])
                print(f'label = {label}')

            #self.message_bus.publish.self.tdac_message.get_d(message_d)

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
