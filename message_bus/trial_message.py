import common
import json

class TrialMessage:

    def __init__(self, message):
        print("TrialMessage.__init__")
        print("message = " + message)
        self.foo = json.loads(message)
