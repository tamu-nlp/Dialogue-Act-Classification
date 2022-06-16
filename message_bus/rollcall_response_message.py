from message import Message
from version import Version

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# This message is written to the Message Bus when we receive a 
# Rollcall Request message
#
# https://gitlab.asist.aptima.com/asist/testbed/-/blob/develop/MessageSpecs/Agent/rollcall/agent_rollcall_response.json

class RollcallResponseMessage(Message):
    topic = 'agent/control/rollcall/response'
    message_type = 'agent'
    sub_type = 'rollcall:response'

    # create a publication dictionary based on the rollcall request dictionary
    def get_d(self, message_bus, rollcall_request_d):
        d = self.get_base_d(rollcall_request_d)
        d['data'] = {
            'status': 'up',
            'version': Version.version, # this application version
            'rollcall_id': rollcall_request_d['data']['rollcall_id'],
            'uptime': message_bus.uptime()
        }

        return d
