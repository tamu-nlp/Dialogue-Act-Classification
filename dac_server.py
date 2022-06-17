import os
from typing import Optional, Dict, List
from dataclasses import dataclass
from pydantic import BaseModel
from inference import Predictor
import argparse


import sys
sys.path.append('message_bus')
from message_bus import MessageBus


#print(os.path.dirname(__file__))

# Get model path
MODEL_PATH = os.path.dirname(__file__) + "./data/sequential_baseline.pt"
#print(MODEL_PATH)


# Create predictor object
PREDICTOR = Predictor(model_path=MODEL_PATH, history_len=7)


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

# MQTT broker network location
class TdacServer:

    def __init__(self, args):
        self.message_bus = MessageBus(self,
            args.host, args.port, args.nochat)

    # The model should reset before and after each mission.
    def reset_model(self):
        PREDICTOR.reset_model()

    # 
    def classify_utterance(self, participant_id, text):
        classification = PREDICTOR.predict(f"{participant_id}:{text}")
        return classification




# If run as a script, take command line args
if __name__ == '__main__':

    # ingest command line args
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-host',
        action='store',
        default = 'localhost',
        help = 'The MQTT broker machine name.')
    parser.add_argument('-port',
        action='store',
        default = 1883,
        help = 'The MQTT broker port number.')
    parser.add_argument('--nochat',
        action='store_true',
        help = 'Do not process Minecraft Chat messages.')
    args = parser.parse_args(sys.argv[1:])

    # start the server
    tdac_server = TdacServer(args)

