from common import Version
import json


class HeartbeatMessage:
    data = {
        "state" : "ok",
        "active" : True,
        "status" : "I am processing messages"
    }

    # default before any messages have been read from the bus
    d = {
        "data" : data,
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

    def __init__(self):
        pass

    def __init__(self, trial_message_dict):
        self.d = {
            "data" : self.data,
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
        trial_sub_type = trial_message_dict["msg"]["sub_type"]
        if(trial_sub_type == "start"):
            trial_id = {"trial_id": trial_message_dict["msg"]["trial_id"]}
            self.d["msg"].update(trial_id)

        # Check for non-null replay_parent_type
        replay_parent_type = trial_message_dict["msg"]["replay_parent_type"]
        if(replay_parent_type != null):
            self.d["msg"].update({"replay_parent_type" : replay_parent_type})

        # Check for non-null replay_id
        replay_id = trial_message_dict["msg"]["replay_id"]
        if(replay_id != null):
            self.d["msg"].update({"replay_id" : replay_id})

        # Check for non-null replay_parent_id
        replay_parent_id = trial_message_dict["msg"]["replay_parent_id"]
        if(replay_parent_id != null):
            self.d["msg"].update({"replay_parent_id" : replay_parent_id})

        return self.d

    # set the same timestamp on the header and msg
    def set_timestamp(self, timestamp):
        self.d['header']['timestamp'] = timestamp
        self.d['msg']['timestamp'] = timestamp
