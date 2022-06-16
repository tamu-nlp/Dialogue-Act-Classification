from message import Message

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# Handle trial start and trial stop messages subscribed from the Message Bus
# by calling trial_start or trial_stop methods of the message_bus class
#

class TrialMessageHandler():
    topic = 'trial'
    message_type = 'trial'

# handle trial_start message
class TrialStartMessageHandler(TrialMessageHandler, Message):
    sub_type = 'start'

    def on_message(self, message_bus, trial_message_d):
        if self.is_subscribed(trial_message_d):
            message_bus.start_trial(trial_message_d)

# handle trial stop message
class TrialStopMessageHandler(TrialMessageHandler, Message):
    sub_type = 'stop'

    def on_message(self, message_bus, trial_message_d):
        if(self.is_subscribed(trial_message_d)):
            message_bus.stop_trial(trial_message_d)
