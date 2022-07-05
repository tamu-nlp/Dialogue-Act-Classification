import argparse
import json
import os
import sys
import traceback
import json
import jsondiff

# Compare two json files and output any differences.

def diff_files(filename1, filename2):
    print('Diffing ' + filename1 + ', ' + filename2)





# exit(1) if file does not exist or does not have .metadata extension
def valid_file(filename):
    # Check that the file exists
    if not os.path.exists(filename):
        print(f'{filename} not found')
        exit(1)

    # make sure it is a regular file or a link to one
    if not os.path.isfile(filename):
        print(f'{filename} must be a .metadata file')
        exit(1)

    # Check for metadata file extension
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
