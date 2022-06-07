import sys
from subscriber import Subscriber
from publisher import Publisher
from heartbeat_publisher import HeartbeatPublisher
from message_handlers import TrialStartMessageHandler
from message_handlers import TrialStopMessageHandler
from message_handlers import RollcallRequestMessageHandler
from message_handlers import AsrMessageHandler
from utils import Utils
from version import Version

# Coordinator class for all things Message Bus
class MessageBus(Utils):

    # shown on startup splash
    name = "TDAC"

    def __init__(self, dac_server, host, port):
        self.dac_server = dac_server

        # init message handlers
        self.message_handlers = [
            AsrMessageHandler(self),
            RollcallRequestMessageHandler(self),
            TrialStartMessageHandler(self),
            TrialStopMessageHandler(self)
        ]

        # connect to the Message Bus
        print(self.name + " is connecting to Message Bus...")
        self.mqtt_url = "tcp://" + host + ":" + str(port)
        self.publisher = Publisher(self, host, port)
        self.subscriber = Subscriber(self, host, port)

    # subscriber has successfully connected to the MQTT broker
    def on_subscriber_connect(self):
        print("Connected to Message Bus at " + self.mqtt_url)
        print(self.name + " version " + Version.version + " running.")
        self.heartbeat_publisher = HeartbeatPublisher(self)

    # publish a classification message based on the input text
    def classify_utterance(self, participant_id, text):
        return self.dac_server.classify_utterance(participant_id, text)

    # reset the model on trial start and stop
    def reset_model(self):
        self.dac_server.reset_model()
    
    # handle incoming message
    def on_message(self, message_d):
        for handler in self.message_handlers:
            handler.on_message(message_d)

    def publish(self, message_d):
        self.publisher.publish(message_d)
