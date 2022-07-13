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
    completed_process = subprocess.run(['gsutil', 'ls', src], capture_output=True)
    if completed_process.returncode == 0:
        output=completed_process.stdout.decode('utf-8')
        lines = output.split('\n')
        for line in lines:
            if len(line) > 0:
                filenames.append(line)

    else:
        print(completed_process.stderr.decode('utf-8'))

    return filenames


#def get_study(report, study):
#    filenames = get_study_filenames(study)
#    report['studies'].append({'name': study,'files':filenames})

def get_tests(report):
    for i in range(0, len(report['studies'])):
        study = report['studies'][i]
        study['tests'] = []
        filenames = get_study_filenames(study['name'])
        for j in range(0, len(filenames)):
            study['tests'].append({'file':filenames[j]})

def get_studies(report, studies):
    report['studies'] = []
    for study in studies:
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
    get_studies(report, args.studies)
    get_tests(report)

    # say report
    present_report(report)
