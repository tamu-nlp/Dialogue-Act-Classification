#!/usr/bin/env python3

import argparse
import json
import os
import sys
import traceback

# Authors:  Joseph Astier, Adarsh Pyarelal
#
# Validate the AC_UAZ_TA1_DialogAgent output by counting the 
# occurance of each message type.

# Keep track of the number of relevant messages
class MessageCounter:

    # relevant message counts
    counts = {}

    # subscribed messages [topic][header.message_type][msg.subtype]
    subscriptions = {
        'agent/control/rollcall/request': {
            'agent': {
                'rollcall:request': 'rollcall_request'
            }
        },
        'minecraft/chat': {
            'chat': {
                'Event:Chat': 'chat'
            }
        },
        'trial': {
            'trial': {
                'start': 'trial_start',
                'stop': 'trial_stop'
            }
        },
        'agent/asr/final': {
            'observation': {
                'asr:transcription': 'asr'
            }
        },
    }

    # published messages [msg.source][topic][header.message_type][msg.subtype]
    publications = {
        'AC_TAMU_TA1_DialogActClassifier': {
            'agent/AC_TAMU_TA1_DialogActClassifier': {
                'event': {
                    'Event:dialogue_act_label': 'tdac'
                }
            },
            'status/AC_TAMU_TA1_DialogActClassifier/heartbeats': {
                'status': {
                    'heartbeat': 'heartbeats'
                }
            },
            'agent/AC_TAMU_TA1_DialogActClassifier/versioninfo': {
                'agent': {
                    'versioninfo': 'version_info'
                }
            },
            'agent/control/rollcall/response': {
                'agent': {
                    'rollcall:response': 'rollcall_response'
                }
            }
        }
    }

    # reset for each instance of this class
    def __init__(self):
        self.counts = {'asr':0, 
            'chat': 0,
            'dialog': 0,
            'heartbeats': 0,
            'num_messages': 0,
            'rollcall_request': 0,
            'rollcall_response': 0,
            'trial_start': 0,
            'version_info': 0,
            'other': 0}

    # Bump the count for the key
    def increment_field(self, key):
        value = 1
        if(key in self.counts):
            value += self.counts[key]
        self.counts.update({key:value})
        self.counts['num_messages'] = self.counts['num_messages']+1

    def count_message(self, message):
        topic = message.get('topic','other')
        message_type = message.get('header',{}).get('message_type','other')
        sub_type = message.get('msg',{}).get('sub_type', 'other')
        source = message.get('msg',{}).get('source', 'other')

        d = self.publications.get(source,self.subscriptions)
        field = d.get(topic,{}).get(message_type,{}).get(sub_type,'other')
        self.increment_field(field)


    # count a line of input which may be anything
    def count_line(self, line):
        self.increment_field('num_lines')
        try:
            self.count_message(json.loads(line))
        except Exception as e:
            line_number = self.counts['num_lines']
            bad_line = line.replace('\n','')
            print(f'Could not parse JSON on line {line_number}: {bad_line}')

# name is the agent name
# lines are single-line JSON messages from the message bus
# table is a global where:
#     key is the id of the test.
#     value is a tuple of [name, success, data, predicate] where:
#         name is the agent name. 
#         success is True if the test passed
#         data is extra data you've given to accompany the result.
#         predicate is a description of the test
#
def ac_uaz_ta1_dialog_agent_test(name,lines,table:dict):

    message_counter = MessageCounter()

    # count the messages
    for line in lines:
        message_counter.count_line(line)

    counts = message_counter.counts

    # string representations of message counts
    asr = str(counts['asr'])
    chat = str(counts['chat'])
    dialog = str(counts['dialog'])
    heartbeats = str(counts['heartbeats'])
    version_info = str(counts['version_info'])
    rc_res = str(counts['rollcall_response'])
    rc_req = str(counts['rollcall_request'])
    trial_start = str(counts['trial_start'])
    num_messages = str(counts['num_messages'])

    # TEST 0:  The number of dialog messages must equal the number
    #          of chat and final ASR messages
    test_id = f'{name}_0'
    success = counts['dialog'] == (counts['asr'] + counts['chat'])
    data = f'# dialog : {dialog}'
    predicate = f'# dialog({dialog}) == chat({chat}) + final({asr})'
    table[test_id] = name, str(success), data, predicate

    # TEST 1:  The number of version_info messages must equal the number
    #          of trial_start messages
    test_id = f'{name}_1'
    success = counts['version_info'] == counts['trial_start']
    data = f'# version_info : {version_info}'
    predicate = f'# version_info({version_info}) == trial_start({trial_start})'
    table[test_id] = name, str(success), data, predicate

    # TEST 2:  The number of rollcall_response messages must equal the
    #          rollcall_request messages
    test_id = f'{name}_2'
    success = counts['rollcall_response'] == counts['rollcall_request']
    data = f'# rollcall_response : {rc_res}'
    predicate = f'# rollcall_response({rc_res}) == rollcall_request({rc_req})'
    table[test_id] = name, str(success), data, predicate

    # TEST 3:  The number of heartbeat messages must be greater than zero
    test_id = f'{name}_3'
    success = counts['heartbeats'] > 0
    data = f'# heartbeats : {heartbeats}'
    predicate = f'# heartbeats({heartbeats}) > 0'
    table[test_id] = name, str(success), data, predicate

    # TEST 4:  The number of messages must be greater than zero
    test_id = f'{name}_4'
    success = counts['num_messages'] > 0
    data = f'# num_messages : {num_messages}'
    predicate = f'# num_messages({num_messages}) > 0'
    if not success:  # a degenerate case, only include if it fails.
        table[test_id] = name, str(success), data, predicate

# test one filename from the command line
def test_metadata_file(filename):

    # simulate the global table used by the Testbed
    table = {}

    input_file = open(filename, 'r', encoding='UTF-8') 
    lines = input_file.readlines()
    ac_uaz_ta1_dialog_agent_test('ac_uaz_ta1_dialog_agent', lines, table)

    # Show the table using the same formatting as the Testbed
    print ("{:<28} {:<28} {:<10} {:<32} {:<30}".format('AC/ASI',
        'Test ID', 'Success', 'Relevent Data', 'Predicate'))
    for k, v in table.items():
        test_id, success, data, predicate = v
        print ("{:<28} {:<28} {:<10} {:<32} {:<30}".format(test_id, 
            k, success, data, predicate))

# If run as a script, test metadata files from the command line
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', 
        action='store', 
        nargs = '+',
        help = 'One or more *.metadata filenames') 
    args = parser.parse_args(sys.argv[1:])

    # process valid input files, warn on others
    for filename in args.filenames:

        print(f'{filename}:')

        # Check that the file exists
        if (os.path.isfile(filename)):
            # Check that it's a metadata file
            if filename.endswith('.metadata'):
                test_metadata_file(filename)
            else:
                print('Input file must have .metadata extension')
        else:
            print('File not found.')

        print('')
