import os
import torch
import numpy as np
from APModel import Predictor
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Utterance(BaseModel):
    spk: str
    sent: str

saved_model_file = "ap_model_finetunedASIST.pt"
predictor = Predictor(saved_model_file, 10)


@app.get("/reset")
async def reset_model():
    predictor.reset()
    return {"Model reset"}

@app.post("/APlabel")
async def get_AP_label(inp: Utterance):
    out = predictor.predict(inp.spk, inp.sent)
    return {"part": out['part'],
            "connect": out['connect']}
