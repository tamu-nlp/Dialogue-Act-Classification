from abc import ABC
import datetime
import re

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# Base class for all published and subscribed message types
#

class Message(ABC):

    source = 'dialog_act_classifier'

    # extending classes override these
    topic = 'not_set'
    message_type = 'not_set'
    sub_type = 'not_set'

    # copy a dictionary field. Remove key if not in source.
    def update_field(self, src, dst, key):
        if(key in dst):
            del dst[key]
        if(key in src):
            value = src[key]
            if(value):
                dst.update({key:value})

    # return a UTC timestamp in format:  YYYY-MM-DDThh:mm:ss.ssssZ
    def timestamp(self):
        tm = datetime.datetime.utcnow()
        p = '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}[.]?[0-9]{4}'
        iso = tm.isoformat(timespec='microseconds')
        timestamp = str(iso)
        m = re.search(p, timestamp)
        if(m == None):
            return timestamp + 'Z' # best guess if no match
        else:
            return m.group(0) + 'Z'

    # return a partial dicationary based on the incoming message
    def get_base_d(self, message_bus, message_d):
        timestamp = self.timestamp()
        d = {
            'topic': self.topic,
            'header': {
                'message_type' : self.message_type,
                'timestamp' : timestamp,
                'version' : '1.0' # default if testbed version not found
            },
            'msg': {
                'source': self.source,
                'sub_type': self.sub_type,
                'timestamp' : timestamp,
                'version' : message_bus.version # this application version
            }
        }

        # update common header incoming header fields
        if 'header' in message_d:
            src = message_d['header']
            dst = d['header']
            self.update_field(src, dst, 'version') # testbed version

        # update common message with incoming common message fields
        if 'msg' in message_d:
            src = message_d['msg']
            dst = d['msg']
            self.update_field(src, dst, 'experiment_id')
            self.update_field(src, dst, 'replay_parent_type')
            self.update_field(src, dst, 'replay_id')
            self.update_field(src, dst, 'replay_parent_id')
            self.update_field(src, dst, 'trial_id')

        return d

    # return true if the class parameters match the message dictionary
    def is_subscribed(self, message_d):
        return ((message_d['topic'] == self.topic)
        and (message_d['header']['message_type'] == self.message_type)
        and (message_d['msg']['sub_type'] == self.sub_type))

