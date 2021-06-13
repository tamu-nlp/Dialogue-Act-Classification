# DA_code

## Installing required packages

`pip install -r requirements.txt`

### Download pre-trained model 

[Shared Drive Link](https://drive.google.com/drive/folders/11Y2Km1y1yDIIfyYaFVeF5cpTNBahUsGr?usp=sharing)

### Helper File (for reference)
`python run_test.py`

### Usage
- Create predictor object

`prd = Predictor(model_path='../model/baseline_model_speaker.pt', history_len=7)`

- call predict() method

`prd.predict(sentence)`

- sentence should be formatted as **SpeakerID:Utterance**

`Example-> Alex:send data to the test vet.`

- For a new dialog, reset the model by calling reset_model()

`prd.reset_model()`