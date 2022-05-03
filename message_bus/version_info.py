from common import CommonHeader
import json


##// published Version Info message
#VersionInfo{
#  testbed = "https://gitlab.asist.aptima.com:5050/asist/testbed/uaz_dialog_agent"
#  topic = "agent/tomcat_textAnalyzer/versioninfo"
#  header {
#    message_type = "agent"
#  }
#  msg {
#    sub_type = "versioninfo"
#    source = "uaz_dialog_agent"
#  }
#  data {
#    agent_name = "uaz_dialog_agent"
#    owner = "University of Arizona"
#  }
#}


class VersionInfo:
    pub_topic = "agent/dialogue_act_classfier/versioninfo"

    def message():
        return "tdac_versioninfo_message"

    def __init__(self, publisher):
        self.publisher = publisher
        print("VersionInfo.__init__")

#        while(True):
#            print("timed loop")
#            self.publisher.publish("heartbeat", "The beat goes on")
#            time.sleep(1)
