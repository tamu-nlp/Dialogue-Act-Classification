import sys
from subscriber import Subscriber
from publisher import Publisher
import datetime

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# TDAC testing with file input
#

class FileTester():

    def __init__(self, tdac, host, port, nochat, config_d):
        self.tdac = tdac

        # connect to the Message Bus
        print(self.name + ' is connecting to Message Bus...')
        print(f'  host = {host}')
        print(f'  port = {port}')

        self.mqtt_url = 'tcp://' + host + ':' + str(port)
        
        # create the publisher and immediately publish init status
        self.publisher = Publisher(self, host, port)
        hm = HeartbeatMessage();
        d = hm.get_init_d()
        self.publish(d)

        # create the subscriber and wait for it to connect
        self.subscriber = Subscriber(self, 
            host, port, nochat, config_d.get('message_bus',{}))

    # subscriber has successfully connected to the MQTT broker
    def on_subscriber_connect(self):
        print('Connected to Message Bus at ' + self.mqtt_url)
        print(self.name + ' version ' + Version.version + ' running.')
        self.heartbeat_publisher = HeartbeatPublisher(self)

    # write to the message_bs
    def publish(self, d):
        self.publisher.publish(d)
