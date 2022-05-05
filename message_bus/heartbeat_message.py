from version import Version
from utils import Utils
import json


class HeartbeatMessage(Utils):
    topic = "dialogue_act_classfier/heartbeat"
    # Default dictionary before any messages have been read from the bus
    d = {
        "data" : {
            "state" : "ok",
            "active" : True,
            "status" : "I am processing messages"
        },
        "header" : {
            "message_type" : "status",
            "timestamp" : "not_set",
            "version" : "not_set"
        },
        "msg" : {
            "experiment_id" : "not_set",
            "source" : "uaz_tdac_agent",
            "sub_type": "heartbeat",
            "timestamp" : "not_set",
            "version": Version.version
        }
    }

    # Set dictionary values from trial message dictionary
    # @param message_d A Trial Message dicationary
    def from_trial_message(self, message_d):

        # update common header
        src = message_d["header"]
        dst = self.d["header"]
        self.update_field(src, dst, "version")

        # update common msg
        src = message_d["msg"]
        dst = self.d["msg"]
        self.update_field(src, dst, "experiment_id")
        self.update_field(src, dst, "replay_parent_type")
        self.update_field(src, dst, "replay_id")
        self.update_field(src, dst, "replay_parent_id")

        if("trial_id") in src:
            self.update_field(src, dst, "trial_id")
        elif("trial_id" in dst):
            del dst["trial_id"]

        return self.d
