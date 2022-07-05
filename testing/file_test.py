import argparse
import json
import os
import sys
import traceback
import json
import jsondiff

# Compare two json files and output any differences.

def diff_files(file1, file2):
    print('Diffing ' + file1 + ', ' + file2)
    return 0

def valid_file(filename):
    # Check that the file exists
    if (os.path.isfile(filename)):
        # Check that it's a metadata file
        if filename.endswith('.metadata'):
            return True
        else:
            print('Input file must have .metadata extension')
            return False
    else:
        print('File not found.')
        return False

# If run as a script, test metadata files from the command line
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('filenames',
        action='store',
        nargs = '+',
        help = 'One or more *.metadata filenames')
    args = parser.parse_args(sys.argv[1:])

    if len(args.filenames) == 2:
        if(valid_file(args.filenames[0])
        and valid_file(args.filenames[1])):
            diff_files(args.filenames[0], args.filenames[1])

    else:
        print('two filenames are required')
