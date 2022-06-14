from message import Message

# Authors:  Joseph Astier, Adarsh Pyarelal


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
