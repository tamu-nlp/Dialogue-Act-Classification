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
    mqtt_host = 'localhost'
    mqtt_port = 1883

    def __init__(self):
        print('TDAC server init')
        self.message_bus = MessageBus(self, self.mqtt_host, self.mqtt_port)

    # The model should reset before and after each mission.
    def reset_model(self):
        PREDICTOR.reset_model()

    # 
    def classify_utterance(self, participant_id, text):
        classification = PREDICTOR.predict(f"{participant_id}:{text}")
        return classification


tdac_server = TdacServer()
