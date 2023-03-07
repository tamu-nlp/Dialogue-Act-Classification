import os
import numpy as np
import requests


if __name__ == '__main__':

    list_sents = [('A', 'this is a sent'), ('B', 'this is another sentence'), ('A', 'this is working'), ('C', 'Testing AP model')]

    for sent in list_sents:
        res = requests.post('http://127.0.0.1:8000/APlabel', json={'spk': sent[0], 'sent': sent[1]})
        print(res.json())
        print()

    res = requests.get('http://127.0.0.1:8000/reset')
    print(res.json())
    