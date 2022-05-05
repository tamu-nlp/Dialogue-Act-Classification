from version import Version
import utils
import json


class HeartbeatMessage (utils.Utils):
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
    # @param tm_d A Trial Message dicationary
    def from_trial_message(self, tm_d):

        # update common header
        src = tm_d["header"]
        dst = self.d["header"]
        self.update_field(src, dst, "version")

        # update common msg
        src = tm_d["msg"]
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

    # set the same timestamp on the header and msg
    def set_timestamp(self, timestamp):
        self.d['header']['timestamp'] = timestamp
        self.d['msg']['timestamp'] = timestamp
