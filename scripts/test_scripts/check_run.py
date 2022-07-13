import argparse
import subprocess
import sys
import json
import uaz_dialog_act_classifier_agent

# Authors:  Joseph Astier, Adarsh Pyarelal

BUCKET_NAME = 'studies.aptima.com/study-3_2022'
GS_BUCKET_PATH=f'gs://{BUCKET_NAME}/'



def test_metadata_file(filename):
    result = {'filename': filename}

    # download the file
    gs_target = f'{GS_BUCKET_PATH}{filename}'
    download_process = subprocess.run(['gsutil', '-m', 'cp', gs_target, '.'])

    if download_process.returncode == 0:
        print(f'Checking file: {filename}')
        # test the file
        results = uaz_dialog_act_classifier_agent.test_metadata_file(filename)

        # add results to global test report
        result['results'] = results

        # delete the file
        delete_process = subprocess.run(['rm',filename])

    else:
        print(f'Could not download f{filename}')
        print(download_process.stderr.decode('utf-8'))

    return result

# Test the files in a single dataset
def test_dataset(dataset_name):
    dataset = {'name': dataset_name, 'metadata':[]}
    gs_target = f'{GS_BUCKET_PATH}*{dataset_name}*.metadata'
    proc = subprocess.run(['gsutil', 'ls', gs_target], capture_output=True)
    if proc.returncode == 0:
        output=proc.stdout.decode('utf-8')
        bucket_filenames = output.split('\n')
        for bucket_filename in bucket_filenames:
            if len(bucket_filename) > 0:
                filename=bucket_filename[len(GS_BUCKET_PATH):]
                dataset['metadata'].append(test_metadata_file(filename))

    else:
        print('No metadata files found')
        # print(proc.stderr.decode('utf-8'))

    return dataset

def report_results(datasets):
    report={'studies':datasets}
    print(json.dumps(report, indent=4, sort_keys=True))

# download metadata studies and test files
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_names', 
        action='store', 
        nargs = '+',
        help = 'One or more Testbed dataset names, e.g. \"TM000nnn\"') 
    args = parser.parse_args(sys.argv[1:])

    # Test all the Testbed datasets specified by the user
    datasets = []
    for dataset_name in args.dataset_names:
        datasets.append(test_dataset(dataset_name))

    # report resuts
    report_results(datasets)
