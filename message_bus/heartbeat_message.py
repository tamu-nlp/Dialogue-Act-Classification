from message import Message

# Authors:  Joseph Astier, Adarsh Pyarelal
# 
# The Heartbeat Message is published to the Message Bus on a fixed interval to
# advise of the runtime status of this application.
# 
# Specification: https://gitlab.asist.aptima.com/asist/testbed/-/blob/develop/MessageSpecs/Status/status.md
#

class HeartbeatMessage(Message):
    topic = 'status/dialog_act_classfier/heartbeat'
    message_type = 'status'
    sub_type = 'heartbeat'

    # create a publication dictionary during initialization
    def get_init_d(self, message_bus):
        d = self.get_base_d(message_bus, {})
        d['data'] = {
            'state' : 'warn',
            'active' : False,
            'status' : 'I am initializing'
        }
        return d

    # create a publication dictionary based on the trial dictionary
    def get_d(self, message_bus, trial_d):
        d = self.get_base_d(message_bus, trial_d)
        d['data'] = {
            'state' : 'ok',
            'active' : True,
            'status' : 'I am processing messages'
        }
        return d
