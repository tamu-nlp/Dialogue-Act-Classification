import argparse
import subprocess
import sys
import json

# Authors:  Joseph Astier, Adarsh Pyarelal

def check_file(filename):
    # download the file
    completed_process = subprocess.run(['gsutil', '-m', 'cp', filename, '.'])

    if completed_process.returncode == 0:
        print(f'Checking file: {filename}')
        # test the file

        # add results to global test report

        # delete the file

    else:
        print(completed_process.stderr.decode('utf-8'))



# return the filenames from one study
def get_study_filenames(study):
    filenames = []
    src=f'gs://studies.aptima.com/study-3_2022/*{study}*.metadata'
    proc = subprocess.run(['gsutil', 'ls', src], capture_output=True)
    if proc.returncode == 0:
        output=proc.stdout.decode('utf-8')
        lines = output.split('\n')
        for line in lines:
            if len(line) > 0:
                filenames.append(line)

    else:
        print(proc.stderr.decode('utf-8'))

    return filenames


# add a list of tests to each study
def prepare_tests(report):
    for i in range(0, len(report['studies'])):
        study = report['studies'][i]
        study['tests'] = []
        study_name = study['name']
        print(f'{study_name}:')
        filenames = get_study_filenames(study_name)
        for j in range(0, len(filenames)):
            print(filenames[j])
            study['tests'].append({'filename':filenames[j]})

# Add a list of studies to the report
def get_studies(report, args):
    report['studies'] = []
    for study in args.studies:
        # add the study name to the element
        report['studies'].append({'name': study})

def present_report(report):
    print(json.dumps(report, indent=4, sort_keys=True))

# download metadata studies and test files
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('studies', 
        action='store', 
        nargs = '+',
        help = 'One or more *.metadata studies') 
    args = parser.parse_args(sys.argv[1:])

    # will contain all testing information 
    report = {}
    get_studies(report, args)
    prepare_tests(report)

    # say report
    present_report(report)
