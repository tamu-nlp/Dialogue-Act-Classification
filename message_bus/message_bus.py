import subscriber
import publisher


class MessageBus():

    def __init__(self):
        print("MessageBus.__init__")
        self.subscriber = subscriber.Subscriber()
        self.publisher = publisher.Publisher()
