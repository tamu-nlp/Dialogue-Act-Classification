import sys
from subscriber import Subscriber
from publisher import Publisher
from heartbeat_publisher import HeartbeatPublisher
from version import Version
from version_info_message import VersionInfoMessage

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# Coordinator class for the interaction between Message Bus and DAC server
#

class MessageBus():

    # shown on startup splash
    name = 'TDAC'

    def __init__(self, dac_server, host, port):
        self.dac_server = dac_server

        # connect to the Message Bus
        print(self.name + ' is connecting to Message Bus...')
        self.mqtt_url = 'tcp://' + host + ':' + str(port)
        self.publisher = Publisher(self, host, port)
        self.subscriber = Subscriber(self, host, port)

    # subscriber has successfully connected to the MQTT broker
    def on_subscriber_connect(self):
        print('Connected to Message Bus at ' + self.mqtt_url)
        print(self.name + ' version ' + Version.version + ' running.')
        self.heartbeat_publisher = HeartbeatPublisher(self)

    # publish a classification message based on the input text
    def classify_utterance(self, participant_id, text):
        return self.dac_server.classify_utterance(participant_id, text)

    def start_trial(self, trial_message_d):
        version_info_message = VersionInfoMessage()
        d = version_info_message.get_d(trial_message_d)
        d['data'] = version_info_message.get_data()
        self.publish(d)

        self.dac_server.reset_model()
        self.heartbeat_publisher.set_message_d(trial_message_d)

    def stop_trial(self, trial_message_d):
        self.dac_server.reset_model()
        self.heartbeat_publisher.set_message_d(trial_message_d)

    def publish(self, published_message_d):
        self.publisher.publish(published_message_d)
