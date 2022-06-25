#!/usr/bin/env python

# Example usage
# -------------
#
#   ./metadata2csv metadataDirectory csvDirectory


import sys
import os
import json
import pandas as pd
from pathlib import Path
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from logging import warning

def main():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

    parser = ArgumentParser(
        description="metadata2csv",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument("dir_path", type=str, nargs="+", help="Input .metadata files directory location")
    args = parser.parse_args()

    dir_path = args.dir_path[0]
    new_dir = args.dir_path[1]
    # print("dir_path ", dir_path)
    # print("new_path ", new_dir)
    if not os.path.isdir(new_dir): 
        os.makedirs(new_dir)
    filenames = os.listdir(dir_path)
    for filename in filenames:
        filepath = os.path.join(dir_path, filename)

        # Parse the filename components
        path = Path(filepath)
        trial=filepath.rpartition("Trial-")[2].split("_")[0]
        team=str(int(filepath.rpartition("Team-")[2].split("_")[0][2:]))
        condbtwn=filepath.rpartition("CondBtwn-")[2].split("_")[0]
        condwin=filepath.rpartition("CondWin-")[2].split("_")[0]

        # Process the file
        with open(filepath) as f:
            initial_timestamp = None
            dialog = []
            i=0
            for line in f:
                # We are only interested in the final transcriptions, not the
                # intermediate ones.
                if '"sub_type":"start"' in line:
                    initial_timestamp = json.loads(line)["msg"]["timestamp"]

                if "asr/final" in line or "userspeech" in line:
                    message = json.loads(line)
                    data = message["data"]
                    timestamp = message["msg"]["timestamp"]

                    timedelta = relativedelta(parse(timestamp), parse(initial_timestamp))
                    relative_timestamp = f"{timedelta.minutes}:{timedelta.seconds}"
                    
                    if "text" in data:
                        text = data["text"]
                        if text == "": i=0
                    else: text = ""
                    if "asr/final" in line and "participant_id" in data:
                        participant_id = data["participant_id"]
                    elif "userspeech" in line and "playername" in data:
                        participant_id = data["playername"]
                    else: participant_id = ""
                    trial_uuid = message["msg"]["trial_id"]
                    if i%2 == 0 and text != "":
                        dialog.append([participant_id, text, relative_timestamp])
                    i+=1

        

        df = pd.DataFrame(dialog)
        df.columns = ["participant", "utt", "start_timestamp"]
        df["end_timestamp"] = ""
        df["corr_utt"] = ""
        filename = filename.split(".")[0]
        new_file_path = os.path.join(new_dir, filename+"_correctedTranscripts.csv")
        df.to_csv(new_file_path, index = False)

    
if __name__ == "__main__":
    main()
    