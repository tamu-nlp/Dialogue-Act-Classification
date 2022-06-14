from message import Message

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# Sent whenever we get a rollcall request message directed to us
#

class RollcallResponseMessage(Message):
    topic = 'agent/control/rollcall/response'
    message_type = 'agent'
    sub_type = 'rollcall:response'

    def get_data(self):
        return {
            'status': 'up'
        }
