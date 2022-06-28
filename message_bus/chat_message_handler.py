from message import Message
from tdac_message import TdacMessage
from config import Config
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

    ignored_senders = []

    # Make sure the sender isn't excluded in the config file
    def sender_valid(self, sender):
        for ignored_sender in self.ignored_senders:
            if ignored_sender == sender:
                return False
        return True

    def read_config(self, message_bus_config_d):
        chat_config_d = message_bus_config_d.get('chat',{})
        self.ignored_senders = chat_config_d.get('ignored_senders',[])
        if len(self.ignored_senders) > 0:
            print('Chat message handler ignoring senders: ')
            for sender in self.ignored_senders:
                print('  ' + sender)

    def __init__(self, config_d):
        self.read_config(config_d)

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
