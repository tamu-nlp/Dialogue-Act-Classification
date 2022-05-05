from common import Version
import utils
import json


class HeartbeatMessage (utils.Utils):

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

    # Set dictionary values from trial message
    def from_trial_message(self, trial_message_d):
        # update the common header
        src = trial_message_d["header"]
        dst = self.d["header"]
        self.update_field(src, dst, "version")

        # update the common msg
        src = trial_message_d["msg"]
        dst = self.d["msg"]
        self.update_field(src, dst,"experiment_id")
        self.update_field(src, dst,"replay_parent_type")
        self.update_field(src, dst,"replay_id")
        self.update_field(src, dst,"replay_parent_id")

        # inclue the trial ID or delete it depending on trial state
        key = "sub_type"
        if(key in src):
            # If it's a trial start, add the trial id
            if (src[key] == "start"):
                self.update_field(src, dst,"trial_id")
            # If it's a trial stop, remove the trial id
            elif ((src[key] == "stop") and ("trial_id" in dst)):
                del(dst["trial_id"])

        return self.d

    # set the same timestamp on the header and msg
    def set_timestamp(self, timestamp):
        self.d['header']['timestamp'] = timestamp
        self.d['msg']['timestamp'] = timestamp
