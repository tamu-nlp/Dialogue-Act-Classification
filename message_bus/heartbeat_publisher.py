import threading
from heartbeat_message import HeartbeatMessage

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# Generates a heartbeat message on the heartbeat interval in a
# seperate non-blocking thread 
#

class HeartbeatPublisher():

    # set > 0 to for regular heartbeats
    heartbeat_interval_seconds = 10

    # used to create heartbeat message dictionaries
    heartbeat_message = HeartbeatMessage()

    # used by heartbeat_message when creating heartbeat message dictionaries
    trial_d = {}

    # Create a heartbeat message and send it off for publishing
    def publish_heartbeat(self):
        d = self.heartbeat_message.get_d(self.message_bus, self.trial_d)
        self.message_bus.publish(d)

    # trigger heartbeats on a preset interval
    def pulse(self, phony):
        ticker = threading.Event()
        while not ticker.wait(self.heartbeat_interval_seconds):
            self.publish_heartbeat()

    # Start the pulse in a seperate thread so MQTT clients are not blocked
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

    # set the message used to create heartbeat messages
    def set_trial_d(self, trial_d):
        self.trial_d = trial_d
        self.publish_heartbeat()
