from message import Message

# Authors:  Joseph Astier, Adarsh Pyarelal
# 
# This message is written to the Message Bus on a fixed interval to advise of
# the runtime status of this application.
# 
# Definition:  
# https://gitlab.asist.aptima.com/asist/testbed/-/blob/develop/MessageSpecs/Status/status.md

class HeartbeatMessage(Message):
    topic = 'agent/dialogue_act_classfier/heartbeat'
    message_type = 'status'
    sub_type = 'heartbeat'

    def get_data(self):
        return {
            'state' : 'ok',
            'active' : True,
            'status' : 'I am processing messages'
        }
