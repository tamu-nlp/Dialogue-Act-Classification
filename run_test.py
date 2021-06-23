from inference import Predictor
import warnings
warnings.filterwarnings('ignore')

examples = """s1:that will allow your microphone to
s2:send data to the test vet.
s3:And I will check that data is coming in meaning.
s1:balkanization Japan music recipe using headphones
s2:Yes.
s1:I am I am not.
s3:You know what? I don't have working headphones right now. Is it coming through? All right.
s1:Give me just a second. Let me see if I can find some.""".split('\n')

prd = Predictor(model_path='../model/baseline_model_speaker.pt', history_len=7)
for i, ex in enumerate(examples):
    if i == 5: prd.reset_model()
    print(ex)
    print(prd.predict(ex))