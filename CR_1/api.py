from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from process_data_copy import process_input
from fastapi import FastAPI
from pydantic import BaseModel
from decode_output import get_clusters
from predict_alt import fetch_model
import sys
import json
import tensorflow as tf
import util


class Utterance(BaseModel):
    spk: str
    sent: str

class Dialog:
    def __init__(self):
        super(Dialog, self).__init__()

        self.reset()

    def reset(self):
        self.text = []

    def accumulate(self, input_utterance):
        self.text.append(input_utterance)
        
        return self.text

model, saver = fetch_model()


app = FastAPI()

dialog = Dialog()

session = tf.Session()
model.restore(session)


@app.get("/reset")
async def reset_model():
    dialog.reset()
    return {"Model reset"}


@app.post("/CoreferenceResolution")

async def get_coreference(inp: Utterance):
    input_str = inp.spk + " says '" + inp.sent + "'"
    text = dialog.accumulate(input_str)
    process_input(text)

    with open('out.jsonlines', "w") as output_file:
        with open('sample.jsonlines') as input_file:
            for example_num, line in enumerate(input_file.readlines()):
                example = json.loads(line)
                tensorized_example = model.tensorize_example(example, is_training=False)
                feed_dict = {i:t for i,t in zip(model.input_tensors, tensorized_example)}
                _, _, _, top_span_starts, top_span_ends, top_antecedents, top_antecedent_scores = session.run(model.predictions, feed_dict=feed_dict)
                predicted_antecedents = model.get_predicted_antecedents(top_antecedents, top_antecedent_scores)
                example["predicted_clusters"], _ = model.get_predicted_clusters(top_span_starts, top_span_ends, predicted_antecedents)
                example["top_spans"] = list(zip((int(i) for i in top_span_starts), (int(i) for i in top_span_ends)))
                example['head_scores'] = []
                
                output_file.write(json.dumps(example))
                output_file.write("\n")
                if example_num % 100 == 0:
                    print("Decoded {} examples.".format(example_num + 1))

    cluster_json = get_clusters('out.jsonlines')
    
    return cluster_json