#!/usr/bin/env python3

import os
from typing import Optional, Dict, List
from dataclasses import dataclass
from pydantic import BaseModel
from inference import Predictor
from config import Config
from version import Version
import argparse
import sys

# local imports
sys.path.append('message_bus')
from message_bus import MessageBus

# Get model path
MODEL_PATH = os.path.dirname(__file__) + "/data/sequential_baseline.pt"

# Create the TDAC instance
class Tdac:

    def __init__(self, args):
        # Create predictor object
        self.predictor = Predictor(model_path=MODEL_PATH, history_len=7)

        config_d = Config().get_d()

    # The model should reset before and after each mission.
    def reset_model(self):
        self.predictor.reset_model()

    # classification for ASR and chat messages, utterance is formatted
    # as 'speaker : text'
    def classify_utterance(self, utterance):
        classification = self.predictor.predict(utterance)
        return classification


# If run as a script, take command line args
if __name__ == '__main__':

    # ingest command line args
    parser = argparse.ArgumentParser(
        description=(
            'Use the TAMU Dialog Act Classifier by entering text at the '
            'command line.  Hit "ENTER" twice to exit the program'
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-o',
        '--output',
        action='store',
        help = 'Write to an output file.'
    )

    args = parser.parse_args(sys.argv[1:])

    # start the application
    tdac = Tdac(args)
    tdac.reset_model()


    version = Version().version
    print(f'TAMU Dialog Act Classifier {version}')
    if args.output:
        print(f'Session will be written to {args.output}')
    print('Enter text for classification at the prompt.')
    print('Press "ENTER" twice to exit the program.')
    print()

    # init output file
    if args.output:
        with open(args.output, "w") as f:
            f.write(f'TAMU Dialog Act Classifier {version}\n\n')

    # number of consecutive times the user has hit enter without a value
    empty_inputs=0

    # Exit the loop if the user hits enter twice in a row
    while not empty_inputs == 2:

        text = input('> ')

        if text == '':
            empty_inputs += 1

        else:
            empty_inputs = 0
            utterance = f'stdin: {text}'
            classification = tdac.classify_utterance(utterance)
            print(f'Classification: {classification}')
            print()

            if(args.output):
                with open(args.output, "a") as f:
                    f.write(f'Text: {text}\n')
                    f.write(f'Classification: {classification}\n\n')

    print('Exiting program.')
    if(args.output):
        with open(args.output, "a") as f:
            f.write('Exiting program.')
