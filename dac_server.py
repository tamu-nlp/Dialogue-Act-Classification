import os
from typing import Optional, Dict, List
from dataclasses import dataclass
from pydantic import BaseModel
from inference import Predictor

import sys
sys.path.append('message_bus')
from message_bus import MessageBus


#print(os.path.dirname(__file__))

# Get model path
MODEL_PATH = os.path.dirname(__file__) + "./data/sequential_baseline.pt"
#print(MODEL_PATH)


# Create predictor object
PREDICTOR = Predictor(model_path=MODEL_PATH, history_len=7)


# create message bus
message_bus = MessageBus()

class DialogAgentMessage(BaseModel):
    """Data model for incoming message from UAZ Dialog Agent"""

    participant_id: str
    text: str
    extractions: List[Dict]


# Define data model for incoming message
class ClassificationMessage(BaseModel):
    """Data model for outgoing message from TAMU Dialog Act Classifier"""

    classification: str

# Create the server instance
#class TdacServer:
#
#    def __init__(self):
#        print("TDAC server init")
#        self.message_bus = MessageBus(self)



