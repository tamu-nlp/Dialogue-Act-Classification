import subscriber
import publisher
import time


# This class manages input and output on the message bus
class MessageBus():


    def __init__(self, dac_server):
        print("MessageBus.__init__")
        self.dac_server = dac_server
        self.publisher = publisher.Publisher()
        self.subscriber = subscriber.Subscriber()
        print("MessageBus.__init__ completed")

        while(True):
            print("timed loop")
            self.publisher.publish("bar", "the bar is open")
            time.sleep(1)

