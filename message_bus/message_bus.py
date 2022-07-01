import sys
from subscriber import Subscriber
from publisher import Publisher
from heartbeat_publisher import HeartbeatPublisher
from version_info_message import VersionInfoMessage
from heartbeat_message import HeartbeatMessage
import datetime

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# Coordinator class for the interaction between Message Bus and DAC server
#

class MessageBus():

    # shown on startup splash
    name = 'TDAC'

    # keep track of when we start so we can compute uptime
    tStart = datetime.datetime.utcnow()

    # return the number of seconds this applicatio has been running
    def uptime(self):
        tNow = datetime.datetime.utcnow()
        dt = tNow - self.tStart
        dt_s = round(dt.total_seconds())

        return dt_s

    def __init__(self, tdac, host, port, nochat, config_d, version):
        self.tdac = tdac
        self.version = version

        # connect to the Message Bus
        print(self.name + ' version ' + version + ' is connecting to Message Bus...')
        print(f'  host = {host}')
        print(f'  port = {port}')

        self.mqtt_url = 'tcp://' + host + ':' + str(port)
        
        # create the publisher and immediately publish init status
        self.publisher = Publisher(self, host, port)
        hm = HeartbeatMessage();
        d = hm.get_init_d(self)
        self.publish(d)

        # create the subscriber and wait for it to connect
        self.subscriber = Subscriber(self, 
            host, port, nochat, config_d.get('message_bus',{}))

    # subscriber has successfully connected to the MQTT broker
    def on_subscriber_connect(self):
        print('Connected to Message Bus at ' + self.mqtt_url)
        print(self.name + ' version ' + self.version + ' running.')
        self.heartbeat_publisher = HeartbeatPublisher(self)

    # publish a classification message based on the input text
    def classify_utterance(self, utterance):
        return self.tdac.classify_utterance(utterance)

    # enter running trial state
    def start_trial(self, trial_d):
        # send version info message
        version_info_message = VersionInfoMessage()
        d = version_info_message.get_d(self, trial_d)
        self.publish(d)

        # reset the TDAC
        self.tdac.reset_model()

        # base heartbeats on the trial message (has trial id)
        self.heartbeat_publisher.set_trial_d(trial_d)

    # enter stopped trial state
    def stop_trial(self, trial_d):

        # reset the TDAC
        self.tdac.reset_model()

        # base heartbeats on the trial message (no trial id)
        self.heartbeat_publisher.set_trial_d(trial_d)

    # write to the message_bs
    def publish(self, d):
        self.publisher.publish(d)

    # return the config object
    def get_config(self):
        return self.config
