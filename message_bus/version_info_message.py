from asr_handler import AsrHandler
from heartbeat_message import HeartbeatMessage
from message import Message
from rollcall_request_handler import RollcallRequestHandler
from rollcall_response_message import RollcallResponseMessage
from tdac_message import TdacMessage
from trial_start_handler import TrialStartHandler
from trial_stop_handler import TrialStopHandler
from version import Version

class VersionInfoMessage (Message):

    # create a message entry for the given message class
    def message_info(message):
        d = {
            "topic": message.topic,
            "message_type": message.message_type,
            "sub_type": message.sub_type
        }
        return d

    topic = "agent/uaz_tdac/versioninfo"
    message_type = "agent"
    sub_type = "versioninfo"
    source = "uaz_tdac_agent"
    data = {
        "agent_name": "uaz_tdac_agent",
        "owner": "University of Arizona",
        "publishes": [
            message_info(TdacMessage),
            message_info(RollcallResponseMessage),
            message_info(HeartbeatMessage),
            {
                "topic": topic,
                "message_type": message_type,
                "sub_type": sub_type
            }
        ],
        "source": [
            "https://gitlab.asist.aptima.com:5050/asist/testbed/"
            + "uaz_tdac_agent:"
            + Version.version
        ],
        "subscribes": [
            message_info(AsrHandler),
            message_info(RollcallRequestHandler),
            message_info(TrialStartHandler),
            message_info(TrialStopHandler)
        ],
        "version": Version.version
    }
