import threading
from heartbeat_message import HeartbeatMessage

# This class generates a heartbeat message on the heartbeat interval in a
# seperate thread that does not block the MQTT clients 
#
# A HeartbeatMessage object is created that persists in memory.
# When the program starts up there is no trial information so default
# data is generated.  When a trial start message is received, the 
# persistent heartbeat message is updated with trial information.  When
# a trial stop message is received, the published heartbeat reverts 
# to default data

class HeartbeatPublisher():

    # set > 0 to for regular heartbeats
    heartbeat_interval_seconds = 10

    # used to create heartbeat message dictionaries
    heartbeat_message = HeartbeatMessage()

    # used by heartbeat_message when creating heartbeat message dictionaries
    message_d = {}

    # Create a heartbeat message and send it off for publishing
    def publish_heartbeat(self):
        d = self.heartbeat_message.get_d(self.message_d)
        d['data'] = self.heartbeat_message.get_data()
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
                "Heartbeat publication interval: " 
                + str(self.heartbeat_interval_seconds)
                + " seconds"
            )
            self.publish_heartbeat() # send a beat immediately
            worker = threading.Thread(target=self.pulse, args=("phony",))
            worker.start()

    # set the message used to create heartbeat messages
    def set_message_d(self, message_d):
        self.message_d = message_d
        self.publish_heartbeat()
