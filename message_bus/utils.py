import datetime
import re

class Utils:

    # copy a dictionary field that may not exist
    def update_field(self, src, dst, key):
        if(key in src):
            value = src[key]
            if(value != None):
                dst.update({key:value})

    # return a UTC timestamp in format:  YYYY-MM-DDThh:mm:ss.ssssZ
    def timestamp(self):
        tm = datetime.datetime.utcnow()
        p = "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}[.]?[0-9]{4}"
        iso = tm.isoformat(timespec='microseconds')
        timestamp = str(iso)
        m = re.search(p, timestamp)
        if(m == None):
            return timestamp + 'Z' # best guess if no match
        else: 
            return m.group(0) + 'Z'

    def topics(self, d):
        f=[]
        for t in d: 
            f.append(t["topic"])
        return set(f)

    # return true if the messages have the same subscription fields
    def is_subscribed(self, d1, d2):
        return ((d1["topic"] == d2["topic"])
        and (d1["header"]["message_type"] == d2["header"]["message_type"])
        and (d1["msg"]["sub_type"] == d2["msg"]["sub_type"]))


        
