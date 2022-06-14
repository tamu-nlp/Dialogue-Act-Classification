from abc import ABC
from version import Version
import datetime
import re

class Message(ABC):

    source = 'dialog_act_classifier'

    # extending classes override these
    topic = "not_set"
    message_type = "not_set"
    sub_type = "not_set"

        # copy a dictionary field that may not exist
    def update_field(self, src, dst, key):
        if(key in dst):
            del dst[key]
        if(key in src):
            value = src[key]
            if(value != None):
                dst.update({key:value})

    # return a UTC timestamp in format:  YYYY-MM-DDThh:mm:ss.ssssZ
    def timestamp(self):
        tm = datetime.datetime.utcnow()
        p = "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}[.]?[0-9]{4}"
        iso = tm.isoformat(timespec='microseconds')
        timestamp = str(iso)
        m = re.search(p, timestamp)
        if(m == None):
            return timestamp + 'Z' # best guess if no match
        else:
            return m.group(0) + 'Z'

    # return a dictionary based on incoming message dictionary
    def get_d(self, message_d):
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

        # update common header incoming header fields
        if 'header' in message_d:
            src = message_d["header"]
            dst = d["header"]
            self.update_field(src, dst, "version")

        # update common message with incoming common message fields
        if 'msg' in message_d:
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
