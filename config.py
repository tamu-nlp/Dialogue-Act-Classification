import argparse
import json
import os
from os.path import exists
import sys
import traceback

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# Settings to configure the Texas A&M Dialog Act Classifier (TDAC) at runtime.
#  
# This class expects file 'config.json' to be in the directory in which
# the TDAC is run.  This file can be in pretty or compact JSON format.
#
# The settings are read into a dictionary that each class needing configuration
# can read

class Config:

    filename = 'scripts/config.json'

    name_key = 'tdac_config'

    # default is an empty library
    d = {}

    def get_d(self):
        return self.d

    # read config settings
    def read_config(self, file_d):
        print('Config.read_config()')
        name = file_d.get('name', '')
        if(name == self.name_key):
            self.d = file_d
        else:
            print('Could not read config, continuing with defaults')


    def __init__(self):
        if exists(self.filename):
            with open(self.filename, 'r', encoding='UTF-8') as json_file:
                try:
                    file_d = json.load(json_file)
                    self.read_config(file_d)
                except ValueError as e:
                    print(f'Error reading JSON config file')

        else:
            print(f'Could not find config file at: {self.filename}')

