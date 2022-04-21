# Authors:  Joseph Astier, Adarsh Pyarelal

# Define message structures used by multiple Testbed message bus message types

# Every testbed message has one of these
class CommonHeader:

    def __init__(self):
        self.timestamp = 'N/A'
        self.message_type = 'N/A'
        self.version = 'N/A'

    def write_json():
        return "JSON"
        

