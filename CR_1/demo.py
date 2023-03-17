import os
import numpy as np
import requests


if __name__ == '__main__':

    list_sents = [('Red', 'Who am I? Testing.'), 
                    ('Green', 'I think we should only buy tools since we can defuse bombs with the tools and not need to communicate.'),
                    ('Blue', 'Hello.'), 
                    ('Green', 'There is 36 bombs in the environment.')]

    for sent in list_sents:
        cluster_json = requests.post('http://127.0.0.1:8000/CoreferenceResolution', json={'spk': sent[0], 'sent': sent[1]})
        print(cluster_json.json())
        print()

    res = requests.get('http://127.0.0.1:8000/reset')
    print(res.json())