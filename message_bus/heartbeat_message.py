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

    # copy common header fields
    def update_header(self, src_d, dst_d):
        src = src_d["header"]
        dst = dst_d["header"]

        self.update_field(src, dst, "version")

    # copy common msg fields
    def update_msg(self, src_d, dst_d):
        src = src_d["msg"]
        dst = dst_d["msg"]

        key = "sub_type"
        if(key in src):
            # If it's a trial start, add the trial id
            if (src[key] == "start"):
                self.update_field(src, dst,"trial_id")
            # If it's a trial stop, remove the trial id
            elif ((src[key] == "stop") and ("trial_id" in dst)):
                del(dst["trial_id"])

        # update fields from trial message
        self.update_field(src, dst,"experiment_id")
        self.update_field(src, dst,"replay_parent_type")
        self.update_field(src, dst,"replay_id")
        self.update_field(src, dst,"replay_parent_id")


    # Set dictionary values from trial message
    def from_trial_message(self, trial_message_d):
        new_d = self.d
        self.update_header(trial_message_d, new_d)
        self.update_msg(trial_message_d, new_d)
        return new_d


    # set the same timestamp on the header and msg
    def set_timestamp(self, timestamp):
        self.d['header']['timestamp'] = timestamp
        self.d['msg']['timestamp'] = timestamp
