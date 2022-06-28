import os
from typing import Optional, Dict, List
from dataclasses import dataclass
from pydantic import BaseModel
from inference import Predictor
from config import Config
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


# Create the server instance
class TdacServer:

    def __init__(self, args):
        config_d = Config().get_d()
        self.message_bus = MessageBus(self,
            args.host, args.port, args.nochat, config_d)

    # The model should reset before and after each mission.
    def reset_model(self):
        PREDICTOR.reset_model()

    # classification for ASR and chat messages, utterance is formatted
    # as 'speaker : text'
    def classify_utterance(self, utterance):
        classification = PREDICTOR.predict(utterance)
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
