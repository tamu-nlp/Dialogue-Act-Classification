from message import Message

class RollcallResponseMessage(Message):
    topic = "agent/control/rollcall/response"
    message_type = "agent"
    sub_type = "rollcall:response"

    def get_data(self):
        return {
            "status": "up"
        }
