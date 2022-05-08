from utils import Utils
from abc import ABC
from version import Version

class Message(ABC, Utils):

    # extending classes set these
    topic = "not_set"
    message_type = "not_set"
    sub_type = "not_set"
    source = "not_set"
    data = {}

    # fields not requiring anything from the Message Bus
    def get_default_d(self):
        timestamp = self.timestamp()
        d = {
            "topic": self.topic,
            "data": self.data,
            "header": {
                "message_type" : self.message_type,
                "timestamp" : timestamp,
            },
            "msg": {
                "message_type": self.message_type,
                "source": self.source,
                "sub_type": self.sub_type,
                "timestamp" : timestamp
            }
        }

        return d

    # update a default dictionary with fields from Message Bus message
    def get_d(self, message_d):

        d = self.get_default_d()

        # update common header
        src = message_d["header"]
        dst = d["header"]
        self.update_field(src, dst, "version")

        # update common message
        src = message_d["msg"]
        dst = d["msg"]
        self.update_field(src, dst, "experiment_id")
        self.update_field(src, dst, "replay_parent_type")
        self.update_field(src, dst, "replay_id")
        self.update_field(src, dst, "replay_parent_id")
        self.update_field(src, dst, "trial_id")

        return d

    # return true this class matches the message class
    def is_subscribed(self, message_d):
        return ((message_d["topic"] == self.topic)
        and (message_d["header"]["message_type"] == self.message_type)
        and (message_d["msg"]["sub_type"] == self.sub_type))
