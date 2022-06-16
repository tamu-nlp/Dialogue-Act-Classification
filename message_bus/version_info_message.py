from asr_message_handler import AsrMessageHandler
from heartbeat_message import HeartbeatMessage
from message import Message
from rollcall_request_message_handler import RollcallRequestMessageHandler
from rollcall_response_message import RollcallResponseMessage
from tdac_message import TdacMessage
from trial_message_handler import TrialStartMessageHandler
from trial_message_handler import TrialStopMessageHandler
from version import Version

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# This message is written to the Message Bus when we receive a Trial Start
# message
# 
# Specification: https://gitlab.asist.aptima.com/asist/testbed/-/blob/develop/MessageSpecs/Agent/versioninfo/agent_versioninfo.md
#

class VersionInfoMessage (Message):

    topic = 'agent/uaz_tdac_agent/versioninfo'
    message_type = 'agent'
    sub_type = 'versioninfo'

    # return a dictionary based on the trial dictionary
    def get_d(self, message_bus, trial_d):
        d = self.get_base_d(trial_d)
        d['data'] = {
            'agent_name': self.source,
            'owner': 'University of Arizona',
            'source': [
                'https://gitlab.asist.aptima.com:5050/asist/testbed/'
                + 'uaz_tdac_agent:'
                + Version.version
            ],
            'publishes': [
                {
                    'topic': self.topic,
                    'message_type': self.message_type,
                    'sub_type': self.sub_type
                },
                {
                    'topic': TdacMessage.topic,
                    'message_type': TdacMessage.message_type,
                    'sub_type': TdacMessage.sub_type
                },
                {
                    'topic': RollcallResponseMessage.topic,
                    'message_type': RollcallResponseMessage.message_type,
                    'sub_type': RollcallResponseMessage.sub_type
                },
                {
                    'topic': HeartbeatMessage.topic,
                    'message_type': HeartbeatMessage.message_type,
                    'sub_type': HeartbeatMessage.sub_type
                }
            ],
            'subscribes': [
                {
                    'topic': AsrMessageHandler.topic,
                    'message_type': AsrMessageHandler.message_type,
                    'sub_type': AsrMessageHandler.sub_type
                },
                {
                    'topic': RollcallRequestMessageHandler.topic,
                    'message_type': RollcallRequestMessageHandler.message_type,
                    'sub_type': RollcallRequestMessageHandler.sub_type
                },
                {
                    'topic': TrialStartMessageHandler.topic,
                    'message_type': TrialStartMessageHandler.message_type,
                    'sub_type': TrialStartMessageHandler.sub_type
                },
                {
                    'topic': TrialStopMessageHandler.topic,
                    'message_type': TrialStopMessageHandler.message_type,
                    'sub_type': TrialStopMessageHandler.sub_type
                }
            ],
            'version': Version.version
        }

        return d
