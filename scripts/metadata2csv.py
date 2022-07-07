#!/usr/bin/env python

# Example usage
# -------------
#
#   ./metadata2csv metadataDirectory csvDirectory


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

    parser.add_argument(
        "dir_path", type=str, nargs="+", help="Input .metadata files directory location"
    )
    args = parser.parse_args()

    dir_path = args.dir_path[0]
    new_dir = args.dir_path[1]

    if not os.path.isdir(new_dir):
        os.makedirs(new_dir)
    filenames = os.listdir(dir_path)
    for filename in filenames:
        filepath = os.path.join(dir_path, filename)

        # Parse the filename components
        path = Path(filepath)
        trial = filepath.rpartition("Trial-")[2].split("_")[0]
        team = str(int(filepath.rpartition("Team-")[2].split("_")[0][2:]))
        condbtwn = filepath.rpartition("CondBtwn-")[2].split("_")[0]
        condwin = filepath.rpartition("CondWin-")[2].split("_")[0]

        # Process the file
        with open(filepath) as f:
            initial_timestamp = None
            dialog = []

            for line in f:
                # grab the timestamp for the trial start
                if '"sub_type":"start"' in line:
                    initial_timestamp = json.loads(line)["msg"]["timestamp"]

                # after grabbing initial timestamp,
                # find all transcribed utterances
                if initial_timestamp is not None:
                    message = json.loads(line)
                    # we want the asr transcriptioins
                    # with topic agent/asr/final
                    if (
                        message["msg"]["sub_type"] == "asr:transcription"
                        and message["topic"] == "agent/asr/final"
                    ):
                        data = message["data"]

                        # calculate start timestamp
                        start_time = data["start_timestamp"]
                        startdelta = relativedelta(
                            parse(start_time), parse(initial_timestamp)
                        )
                        relative_start = f"{startdelta.minutes}:{startdelta.seconds}"

                        # calculate end timestamp
                        end_time = data["end_timestamp"]
                        enddelta = relativedelta(
                            parse(end_time), parse(initial_timestamp)
                        )
                        relative_end = f"{enddelta.minutes}:{enddelta.seconds}"

                        # get the text, utt id, and participant id
                        text = data["text"]
                        msg_id = data["id"]
                        participant_id = data["participant_id"]

                        # add these items to the dialog
                        dialog.append(
                            [msg_id, participant_id, text, relative_start, relative_end]
                        )

        # convert dialog to pandas df
        df = pd.DataFrame(dialog)

        # add colnames and empty col
        # for manual transcript correction
        df.columns = [
            "message_id",
            "participant",
            "utt",
            "start_timestamp",
            "end_timestamp",
        ]
        df["corr_utt"] = ""

        # save this csv
        filename = filename.split(".")[0]
        new_file_path = os.path.join(new_dir, filename + "_correctedTranscripts.csv")
        df.to_csv(new_file_path, index=False)


if __name__ == "__main__":
    main()
