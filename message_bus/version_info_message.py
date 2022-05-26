from message_handlers import AsrMessageHandler
from heartbeat_message import HeartbeatMessage
from message import Message
from message_handlers import RollcallRequestMessageHandler
from rollcall_response_message import RollcallResponseMessage
from tdac_message import TdacMessage
from message_handlers import TrialStartMessageHandler
from message_handlers import TrialStopMessageHandler
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

    topic = "agent/uaz_tdac_agent/versioninfo"
    message_type = "agent"
    sub_type = "versioninfo"
    source = "uaz_tdac_agent"
    data = {
        "agent_name": source,
        "owner": "University of Arizona",
        "publishes": [
            {
                "topic": topic,
                "message_type": message_type,
                "sub_type": sub_type
            },
            message_info(TdacMessage),
            message_info(RollcallResponseMessage),
            message_info(HeartbeatMessage)
        ],
        "source": [
            "https://gitlab.asist.aptima.com:5050/asist/testbed/"
            + "uaz_tdac_agent:"
            + Version.version
        ],
        "subscribes": [
            message_info(AsrMessageHandler),
            message_info(RollcallRequestMessageHandler),
            message_info(TrialStartMessageHandler),
            message_info(TrialStopMessageHandler)
        ],
        "version": Version.version
    }
