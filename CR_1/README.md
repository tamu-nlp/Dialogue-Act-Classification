# BERT and SpanBERT for Coreference Resolution
This repository contains code and models for the paper, [BERT for Coreference Resolution: Baselines and Analysis](https://arxiv.org/abs/1908.09091). Additionally, it contains the coreference resolution model from the paper [SpanBERT: Improving Pre-training by Representing and Predicting Spans](https://arxiv.org/abs/1907.10529), which achieves 79.6 F1 on OntoNotes 79.6 F1. 

The model architecture itself is an extension of the [e2e-coref](https://github.com/kentonl/e2e-coref) model.

The repository is adapted to work in an online mode for ASIST data.

##Instructions to run the code - 
* Create a python3 virtual environment (3.6.9)
* Install python3 requirements: `pip3 install -r requirements_python3.txt`
* A folder containing models, data and data converter scripts called 'data_dir' is required to be downloaded and placed in the same directory. data_dir folder can be downloaded from here: https://drive.google.com/drive/folders/1wgcDdGmigp1_v2M1ztC-BEh8Xo8zU0wZ?usp=share_link
* Prediction on ASIST data will require pasting the dialog in the process_data.py file.
* Then 3 codes are needed to be run consecutively. Commands-
* python3 process_data.py
* python3 predict.py _ sample.jsonlines out.jsonlines
* python3 decode_output.py
* To run the api, uvicorn api:app --reload


@article{joshi2019spanbert,
    title={{SpanBERT}: Improving Pre-training by Representing and Predicting Spans},
    author={Mandar Joshi and Danqi Chen and Yinhan Liu and Daniel S. Weld and Luke Zettlemoyer and Omer Levy},
    year={2019},
    journal={arXiv preprint arXiv:1907.10529}
}
