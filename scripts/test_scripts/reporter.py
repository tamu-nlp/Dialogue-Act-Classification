import argparse
import subprocess
import sys
import json

# Authors:  Joseph Astier, Adarsh Pyarelal

# summarize the results of testbed metadata testing
def summarize(report):
    n_


# download metadata studies and test files
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Summarize a test report.')

    parser.add_argument(
        'input', 
        action='store', 
        nargs = '+',
        help = 'Test report file in the correct JSON format'
    ) 

    # Optionally write the test results to a JSON file
    parser.add_argument(
        '-o',
        '--output',
        help = 'Write report to this filename'
    )

    args = parser.parse_args(sys.argv[1:])

    with open(args.input, 'r') as input_file:
        report = json.load(input_file)
        summary = summarize(report, args)
        print(json.dumps(report, indent=4, sort_keys=True))

        if args.output:
            with open(args.output, "w") as output:
                output.write(json.dumps(report indent=4, sort_keys=True)+"\n")

