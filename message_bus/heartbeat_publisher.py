import threading
from heartbeat_message import HeartbeatMessage

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# publishes a heartbeat message in a separate thread on the heartbeat
# interval. 
#

class HeartbeatPublisher():

    # set > 0 to for regular heartbeats
    heartbeat_interval_seconds = 10

    # used to create heartbeat message dictionaries
    heartbeat_message = HeartbeatMessage()

    # trial message used to create heartbeat message dictionaries
    trial_d = {}

    # Create a heartbeat message and publish it to the Message Bus
    def publish_heartbeat(self):
        d = self.heartbeat_message.get_d(self.message_bus, self.trial_d)
        self.message_bus.publish(d)

    # trigger heartbeats on a preset interval
    def pulse(self, phony):
        ticker = threading.Event()
        while not ticker.wait(self.heartbeat_interval_seconds):
            self.publish_heartbeat()

    # Start the heartbeat pulse worker thread
    def __init__(self, message_bus):
        self.message_bus = message_bus
        if(self.heartbeat_interval_seconds > 0):
            print(
                'Heartbeat publication interval: ' 
                + str(self.heartbeat_interval_seconds)
                + ' seconds'
            )
            self.publish_heartbeat() # send a beat immediately
            worker = threading.Thread(target=self.pulse, args=('phony',))
            worker.start()

    # set the trial message used to create heartbeat messages
    def set_trial_d(self, trial_d):
        self.trial_d = trial_d
        self.publish_heartbeat()
