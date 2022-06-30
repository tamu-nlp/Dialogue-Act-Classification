TAMU Dialogue Act Classifier  (TDAC)
============================


Installation
------------

If you want to use the classifier in a Docker continer, skip to the
'With Docker' section below. Otherwise, read on.

You can install the dependencies and download the pretrained model by running

    ./scripts/install

Usage
-----

The Classifier runs on the Message Bus and publishes to the following topics:

```
agent/uaz_tdac_agent/versioninfo
agent/dialog_act_classifier
agent/control/rollcall/response
agent/dialogue_act_classfier/heartbeat
```
Subscriptions from the Message Bus:
```
agent/asr/final
agent/control/rollcall/request
trial
minecraft/chat
```


#### Without Docker

You can run the dialogue act classifier on a Linux operating system with:

    ./scripts/run_dac_server


#### With Docker

To run the classifier in a Docker container, use the following:

    docker-compose up --build
    

#### Command line arguments
The Classifier can be invoked with the following optional command line arguments
```
--host HOST  The MQTT broker machine name. (default: localhost)
--port PORT  The MQTT broker port number. (default: 1883)
--nochat     Do not process Minecraft Chat messages. (default: False)
```

### Python API

The files `inference.py` and `baseline_model.py` need to be in the same
directory (we have not yet set it up as a package, e.g., with a `setup.py`).

````
# Import the required class
from inference import Predictor

# Create predictor object
prd = Predictor(model_path=<path_to_pretrained_pytorch_model>, history_len=7)

# Get prediction using the 'predict' method. The input string should be
formatted as "<speaker_id>:<utterance>"
sentence="Participant 21:Five because at least I know there was one yellow
victim that died so"

classification = prd.predict("<speaker_id>:<utterance>")
print(classification)
# This should print out a classification label, e.g. "Statement"

# For a new dialog, reset the model by calling reset_model()
prd.reset_model()
````

### Testing

The directory `test_data` contains metadata files for each Testbed message type, and scripts to publish each on the Message Bus.  Invoking these scripts will test each subscribed channel of the Classifier.


Performance of the classifier on the MRDA corpus
------------------------------------------------

The table below shows the performance of the classifier on the 
[MRDA Corpus](https://aclanthology.org/W04-2319.pdf)

```
Epoch:  14 Discourse Act Classification Loss:  3469.8051283061504 Time Elapsed:  776.1403894424438
MACRO:  (0.3743169297633522, 0.3400945782484077, 0.34510218344540217, None)
MICRO:  (0.6255096452260694, 0.6255096452260694, 0.6255096452260694, None)
-------------------Test start-----------------------
MACRO:  (0.3812146930074515, 0.36333672165776454, 0.3563412477824784, None)
MICRO:  (0.6382469165369417, 0.6382469165369417, 0.6382469165369417, None)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Classification Report
               precision    recall  f1-score   support

           0       0.00      0.00      0.00        35
           1       0.52      0.42      0.46       134
           2       0.26      0.07      0.11        82
           3       0.44      0.74      0.55       160
           4       0.57      0.45      0.50       531
           5       0.00      0.00      0.00        38
           6       0.27      0.11      0.15       133
           7       0.47      0.28      0.35       402
           8       0.17      0.07      0.10        30
           9       0.00      0.00      0.00         2
          10       0.27      0.67      0.39         9
          11       0.00      0.00      0.00        56
          12       0.50      0.82      0.62        98
          13       0.00      0.00      0.00        17
          14       0.73      0.86      0.79        56
          15       0.58      0.30      0.40       516
          16       0.79      0.79      0.79       350
          17       0.00      0.00      0.00        36
          18       0.88      0.83      0.85        46
          19       0.43      0.69      0.53        39
          20       0.77      0.95      0.85        66
          21       0.33      0.06      0.10        18
          22       0.31      0.24      0.27        17
          23       0.00      0.00      0.00        45
          24       0.00      0.00      0.00        27
          25       0.50      0.33      0.40       136
          26       0.49      0.33      0.39       540
          27       0.45      0.27      0.34        51
          28       0.70      0.48      0.57       354
          29       0.58      0.61      0.59       492
          30       0.75      0.81      0.78      2175
          32       0.00      0.00      0.00        67
          33       0.59      0.61      0.60      1031
          34       0.00      0.00      0.00        22
          35       0.65      0.83      0.73      4971
          36       0.00      0.00      0.00        14
          37       0.44      0.51      0.47        97
          38       0.53      0.38      0.44        26
          39       0.56      0.52      0.54       903
          40       0.64      0.78      0.70         9
          41       0.47      0.38      0.42        90
          42       0.79      0.75      0.77      1520
          43       0.27      0.06      0.10        48
          44       0.66      0.88      0.75       152
          45       0.35      0.50      0.41        12
          46       0.00      0.00      0.00        13
          47       0.53      0.38      0.44       371
          48       0.20      0.05      0.08        42
          49       0.55      0.32      0.40        66
          50       0.42      0.41      0.42       489
          51       0.06      0.01      0.02        68

    accuracy                           0.64     16702
   macro avg       0.38      0.36      0.36     16702
weighted avg       0.61      0.64      0.62     16702
```
