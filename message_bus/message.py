from utils import Utils
from abc import ABC
from version import Version

class Message(ABC, Utils):

    source = 'dialog_act_classifier'

    # extending classes override these
    topic = "not_set"
    message_type = "not_set"
    sub_type = "not_set"

    def get_default_d(self):
        timestamp = self.timestamp()
        d = {
            "topic": self.topic,
            "header": {
                "message_type" : self.message_type,
                "timestamp" : timestamp,
            },
            "msg": {
                "source": self.source,
                "sub_type": self.sub_type,
                "timestamp" : timestamp,
                "version" : Version.version # this application version
            }
        }

    def get_d(self, message_d):
        d = get_default_d()

        # update common header with possibly non-existant data
        src = message_d["header"]
        dst = d["header"]
        self.update_field(src, dst, "version")

        # update common message with possibly non-existant data
        src = message_d["msg"]
        dst = d["msg"]
        self.update_field(src, dst, "experiment_id")
        self.update_field(src, dst, "replay_parent_type")
        self.update_field(src, dst, "replay_id")
        self.update_field(src, dst, "replay_parent_id")
        self.update_field(src, dst, "trial_id")

        return d

    # return true if the class parameters match the message dict parameters
    def is_subscribed(self, message_d):
        return ((message_d["topic"] == self.topic)
        and (message_d["header"]["message_type"] == self.message_type)
        and (message_d["msg"]["sub_type"] == self.sub_type))
