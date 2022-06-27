from message import Message
from tdac_message import TdacMessage
import json

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# Handle a Minecraft Chat message subscribed from the Message Bus by 
# publishing a TDAC Message based on the message text
#
# Chat messages are sent to the xxxx in format 'sender: text'
#

class ChatMessageHandler(Message):
    topic = 'minecraft/chat'
    message_type = 'chat'
    sub_type = 'Event:Chat'

    tdac_message = TdacMessage()

    # Make sure the sender isn't excluded in the config file
    def sender_valid(self, sender):
        # hardcoded at the moment for bench testing
        if sender == 'Server':
            print(f'Chat sender {sender} is excluded')
            return False
        print(f'Chat sender {sender} is included **********')
        return True


    # publish a TDAC dictionary based on the Chat dictionary
    def on_message(self, message_bus, chat_d):
        if self.is_subscribed(chat_d):
            sender = chat_d['data']['sender']
            if self.sender_valid(sender):
                text_json = json.loads(chat_d['data']['text'])
                utterance = sender + ':' + text_json['text']
                print(f'utterance = {utterance}')
                d = self.tdac_message.get_d(message_bus, utterance, chat_d)
                message_bus.publish(d)
