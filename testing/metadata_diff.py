import argparse
import json
import os
import sys
import traceback
import json
import jsondiff

# Compare two json files and output any differences.


# return all the lines from one file
def lines_from_file(filename):
    try:
        with open(filename, 'r', encoding='UTF-8') as input_file:
            return input_file.readlines()

    except IOError:
        print (f'could not read lines from {filename}')
        return ()

def diff_pair(i, line0, line1):

    json0 = json.loads(line0)
    json1 = json.loads(line1)

    d = jsondiff.diff(json0, json1, syntax='symmetric' )

    if d:
        print(f'Line {i}:')
        print(f'{line0}')
        print(f'{line1}')
        print(json.dumps(d))
        return 1

    else:
        return 0
    


def diff_files(filename0, filename1):
    lines0 = lines_from_file(args.filenames[0])
    lines1 = lines_from_file(args.filenames[1])
    len0 = len(lines0)
    len1 = len(lines1)

    print(f'diffing {filename0}, {filename1}')

    # bail out of line lists are not equal length
    if len0 != len1:
        print('Files do not contain the same number of lines')
        print(f' Lines in {filename0}: {len0}')
        print(f' Lines in {filename1}: {len1}')
        exit(1)

    # line pairs that had differences
    diffs = 0

    for x in range(len0):
        diffs += diff_pair(x, lines0[x], lines1[x])

    print(f'Lines tested: {len0}')
    print(f'Non-matching: {diffs}')

    if diffs == 0:
        exit(0)
    else:
        exit(1)

# exit(1) if file does not exist or does not have .metadata extension
def valid_file(filename):

    # File must exist
    if not os.path.exists(filename):
        print(f'{filename} not found')
        exit(1)

    # File must be a regular file or a link to one
    if not os.path.isfile(filename):
        print(f'{filename} must be a .metadata file')
        exit(1)

    # File must have .metadata extension
    if not filename.endswith('.metadata'):
        print(f'{filename} must have .metadata extension')
        exit(1)


# if run as a script, test metadata files from the command line
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('filenames',
        action='store',
        nargs = '+',
        help = 'One or more *.metadata filenames')
    args = parser.parse_args(sys.argv[1:])

    if len(args.filenames) == 2:
        valid_file(args.filenames[0])
        valid_file(args.filenames[1])

        diff_files(args.filenames[0], args.filenames[1])

    else:
        print('two filenames are required')
        exit(1)
