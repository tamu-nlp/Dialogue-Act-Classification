import os
from typing import Optional, Dict, List
from dataclasses import dataclass

from fastapi import FastAPI
from pydantic import BaseModel

from inference import Predictor

# Get model path
MODEL_PATH = os.path.dirname(__file__) + "/data/baseline_model_speaker.pt"

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


# Create the FastAPI instance
app = FastAPI(title="TAMU Dialogue Act Classifier", version="0.0.1")


@app.get("/classify", response_model=str)
def classify_utterance(message: DialogAgentMessage):
    classification = PREDICTOR.predict(
        f"{message.participant_id}:{message.text}"
    )
    # TODO - change this so that the model is reset before each mission,
    # instead of after each utterance. This should probably be done with
    # another API endpoint.
    PREDICTOR.reset_model()
    return classification
