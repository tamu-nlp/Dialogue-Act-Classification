import argparse
import json
import os
import sys
import traceback
import json
import jsondiff

# Compare two json files and output any differences.

def test_files(file1, file2):
    print('Testing ' + file1 + ', ' + file2)

# If run as a script, test metadata files from the command line
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('filenames',
        action='store',
        nargs = '+',
        help = 'One or more *.metadata filenames')
    args = parser.parse_args(sys.argv[1:])

    if len(args.filenames) == 2:
        test_files(args.filenames[0], args.filenames[1])
    else:
        print('two filenames are required')

    # process valid input files, warn on others
    if False:

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

