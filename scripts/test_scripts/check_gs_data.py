import argparse
import subprocess
import sys
import json
import ac_tamu_ta1_dialog_act_classifier

# Authors:  Joseph Astier, Adarsh Pyarelal

# Download testbed data from the Google Cloud and validate using the Testbed 
# test script for this agent

BUCKET = 'studies.aptima.com/study-3_2022'
GS_BUCKET_PATH=f'gs://{BUCKET}/'


def test_metadata_file(filename, args):
    result = {'filename': filename}

    # download the file
    gs_target = f'{GS_BUCKET_PATH}{filename}'
    download_process = subprocess.run(['gsutil', '-m', 'cp', gs_target, '.'])

    if download_process.returncode == 0:
        print(f'Checking file: {filename}')
        # test the file
        results = ac_tamu_ta1_dialog_act_classifier.test_metadata_file(filename)

        # add results to global test report
        result['results'] = results

        # delete the file
        if args.delete:
            delete_process = subprocess.run(['rm',filename])

    else:
        print(f'Could not download f{filename}')
        print(download_process.stderr.decode('utf-8'))

    return result

# Test the files in a single dataset
def test_dataset(dataset_name, args):
    result = {'name': dataset_name, 'metadata':[]}
    gs_target = f'{GS_BUCKET_PATH}*{dataset_name}*.metadata'
    print(f'downloading {gs_target}')
    proc = subprocess.run(['gsutil', 'ls', gs_target], capture_output=True)
    if proc.returncode == 0:
        output=proc.stdout.decode('utf-8')
        bucket_filenames = output.split('\n')
        for bucket_filename in bucket_filenames:
            if len(bucket_filename) > 0:
                filename=bucket_filename[len(GS_BUCKET_PATH):]
                result['metadata'].append(test_metadata_file(filename, args))

    else:
        print('No metadata files found')
        # print(proc.stderr.decode('utf-8'))

    return result

def report_results(report, args):
    print(json.dumps(report, indent=4, sort_keys=True))

    if args.output:
        print(f'Writing results to {args.output}')
        output_file = open(args.output, "w", buffering=1)
        output_file.write(json.dumps(report)+"\n")
        output_file.close()


# download metadata studies and test files
if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument(
        'datasets', 
        action='store', 
        nargs = '+',
        help = 'One or more dataset names, e.g. \"TM000nnn\"'
    ) 

    # Optionally write the test results to a JSON file
    parser.add_argument(
        '-o',
        '--output',
        help = 'Output filename'
    )

    # Optionally do not delete downloaded .metadata files
    parser.add_argument(
        '-d',
        '--delete',
        action="store_true",
        help = 'Delete downloaded .metadata files after testing'
    )

    args = parser.parse_args(sys.argv[1:])

    # Test all the Testbed datasets specified by the user
    report = {'bucket':BUCKET, 'datasets':[]}
    for dataset in args.datasets:
        report['datasets'].append(test_dataset(dataset, args))

    # report resuts
    report_results(report, args)
