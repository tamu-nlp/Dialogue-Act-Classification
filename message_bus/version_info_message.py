from message import Message
from version import Version 
from heartbeat_message import HeartbeatMessage
from rollcall_response_message import RollcallResponseMessage

class VersionInfoMessage (Message):
    topic = "agent/uaz_tdac/versioninfo"
    message_type = "agent"
    sub_type = "versioninfo"
    source = "uaz_tdac_agent",
    data = {
        "agent_name": "uaz_tdac_agent",
        "owner": "University of Arizona",
        "publishes": [
            {
                "topic": "agent/uaz_tdac",
                "message_type": "event",
                "sub_type": "Event:tdac_event"
            },
            {
                "topic": RollcallResponseMessage.topic,
                "message_type": RollcallResponseMessage.message_type,
                "sub_type": RollcallResponseMessage.sub_type
            },
            {
                "topic": topic,
                "message_type": message_type,
                "sub_type": sub_type
            },
            {
                "topic": HeartbeatMessage.topic,
                "message_type":  HeartbeatMessage.message_type,
                "sub_type":  HeartbeatMessage.sub_type
            }
        ],
        "source": [
            "https://gitlab.asist.aptima.com:5050/asist/testbed/"
            + "uaz_tdac_agent:"
            + Version.version
        ],
        "subscribes": [
            {
                "topic": "trial",
                "message_type": "trial",
                "sub_type": "start"
            },
            {
                "topic": "trial",
                "message_type": "trial",
                "sub_type": "stop"
            },
            {
                "topic": "agent/asr/final",
                "message_type": "observation",
                "sub_type": "asr:transcription"
            },
            {
                "topic": "agent/control/rollcall/request",
                "message_type": "agent",
                "sub_type": "rollcall:request"
            }
        ],
        "version": Version.version
    }
