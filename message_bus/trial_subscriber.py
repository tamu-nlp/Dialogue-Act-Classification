import paho.mqtt.client as mqtt
import json

class TrialSubscriber:

    def on_trial_message(self, trial_message_dict):
        print("TrialSubscriber.on_trial_message")
        print(json.dumps(trial_message_dict, indent=2))


    def __init__(self, message_bus):
        self.message_bus = message_bus
