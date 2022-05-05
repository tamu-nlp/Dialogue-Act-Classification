from common import Version
import json


class HeartbeatMessage:

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
    def from_trial_message(self, trial_message_dict):
        self.d = {
            "data" : {
                "state" : "ok",
                "active" : True,
                "status" : "I am processing messages"
            },
            "header" : {
                "message_type" : "status",
                "timestamp" : "not_set",
                "version" : trial_message_dict["header"]["version"]
            },
            "msg" : {
                "experiment_id" : trial_message_dict["msg"]["experiment_id"],
                "source" : "uaz_tdac_agent",
                "sub_type": "heartbeat",
                "timestamp" : "not_set",
                "version": Version.version
            }
        }

        # If it's a trial start, add the trial id
        if ("sub_type" in trial_message_dict["msg"]):
            v = trial_message_dict["msg"]["sub_type"]
            if(v == "start"):
                kv = {"trial_id": trial_message_dict["msg"]["trial_id"]}
                self.d["msg"].update(kv)

        # Check for non-null replay_parent_type
        if ("replay_parent_type" in trial_message_dict["msg"]):
            v = trial_message_dict["msg"]["replay_parent_type"]
            if(v != None):
                kv =({"replay_parent_type" : replay_parent_type})
                self.d["msg"].update(kv)

        # Check for non-null replay_id
        if ("replay_id" in trial_message_dict["msg"]):
            v = trial_message_dict["msg"]["replay_id"]
            if(v != None):
                kv = ({"replay_id" : replay_id})
                self.d["msg"].update(kv)

        # Check for non-null replay_parent_id
        if ("replay_parent_id" in trial_message_dict["msg"]):
            v = trial_message_dict["msg"]["replay_parent_id"]
            if(v != None):
                kv = ({"replay_parent_id" : replay_parent_id})
                self.d["msg"].update(kv)

        return self.d

    # set the same timestamp on the header and msg
    def set_timestamp(self, timestamp):
        self.d['header']['timestamp'] = timestamp
        self.d['msg']['timestamp'] = timestamp
