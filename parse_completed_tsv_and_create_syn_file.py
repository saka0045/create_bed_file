#!/usr/bin/python3

"""
This script parses the list of transcripts and adds the gene name from the Alamut tsv file to create
the os.syn file required to use Rohan's OS scripts
"""


import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--inputTsvFile", dest="input_tsv_file_path"
    )
    parser.add_argument(
        "-s", "--synonymFile", dest="syn_file_path"
    )
    parser.add_argument(
        "-o", "--outSynFile", dest="out_syn_file_path",
        help="Complete file path to the desired output file"
    )

    args = parser.parse_args()

    tsv_file_path = os.path.abspath(args.input_tsv_file_path)
    syn_file_path = os.path.abspath(args.syn_file_path)
    out_syn_file_path = os.path.abspath(args.out_syn_file_path)

    tsv_file = open(tsv_file_path, "r")
    syn_file = open(syn_file_path, "r")
    out_syn_file = open(out_syn_file_path, "w")

    # Go through the list of transcripts and store them in a list
    syn_file_transcript_list = []
    for syn_transcript in syn_file:
        syn_transcript = syn_transcript.rstrip()
        if syn_transcript not in syn_file_transcript_list:
            syn_file_transcript_list.append(syn_transcript)
        # If duplicate transcripts are found in the list of transcripts, abort the script
        else:
            sys.exit("Found duplicate entry for " + syn_transcript)

    # Parse through the Alamut style tsv file
    # Ignore header line
    tsv_file.readline()
    tsv_file_dict = {}
    abnormal_transcripts = []
    for line in tsv_file:
        line = line.rstrip()
        tsv_line_item = line.split("\t")
        tsv_gene = tsv_line_item[1]
        tsv_transcript = tsv_line_item[7]
        # Keep track of abnormal transcripts that contain two underscores "_"
        if tsv_transcript.count("_") >= 2:
            if tsv_transcript not in abnormal_transcripts:
                abnormal_transcripts.append(tsv_transcript)
        if tsv_transcript not in tsv_file_dict.keys():
            tsv_file_dict[tsv_transcript] = tsv_gene

    print("Number of transcripts in the transcript file is " + str(len(syn_file_transcript_list)))
    print("Number of transcripts in the tsv file is " + str(len(tsv_file_dict)))

    if len(syn_file_transcript_list) != len(tsv_file_dict):
        print("Transcripts in syn file not in tsv file: ")
        for transcript in syn_file_transcript_list:
            if transcript not in tsv_file_dict.keys():
                print(transcript)

    # Create the out syn file
    for tsv_transcript, tsv_gene in tsv_file_dict.items():
        out_syn_file.write(tsv_gene + "\t" + tsv_transcript + "\n")

    tsv_file.close()
    syn_file.close()
    out_syn_file.close()


if __name__ == "__main__":
    main()
