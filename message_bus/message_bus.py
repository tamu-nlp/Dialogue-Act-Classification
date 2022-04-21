import subscriber
import publisher
import time


class MessageBus():


    def __init__(self):
        print("MessageBus.__init__")
        self.publisher = publisher.Publisher()
        self.subscriber = subscriber.Subscriber()
        print("MessageBus.__init__ completed")

        while(True):
            print("timed loop")
            time.sleep(1)

