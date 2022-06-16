from message import Message
from tdac_message import TdacMessage

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# Handle a Minecraft Chat message subscribed from the Message Bus by 
# publishing a TDAC Message based on the message text
#

class ChatMessageHandler(Message):
    topic = 'minecraft/chat'
    message_type = 'chat'
    sub_type = 'Event:Chat'

    tdac_message = TdacMessage()

    # publish a TDAC dictionary based on the Chat dictionary
    def on_message(self, message_bus, chat_d):
        if(self.is_subscribed(chat_d)):
            sender = chat_d['data']['sender']
            text_d = eval(chat_d['data']['text'])
            text = text_d['text']
            tdac_d = self.tdac_message.get_d(message_bus,
                sender, text, chat_d)
            message_bus.publish(tdac_d)
