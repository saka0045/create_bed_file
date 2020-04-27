#!/usr/bin/python3

"""
This script parses the list of transcripts and adds the gene name from the Alamut tsv file to create
the os.syn file required to use Rohan's OS scripts
"""


import argparse
import os
import sys
from parse_ncbi_file import parse_tsv_file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--inputTsvFile", dest="input_tsv_file_path"
    )
    parser.add_argument(
        "-c", "--candidateTranscriptFile", dest="candidate_transcript_file_path"
    )
    parser.add_argument(
        "-o", "--outSynFile", dest="out_syn_file_path",
        help="Complete file path to the desired output file"
    )

    args = parser.parse_args()

    tsv_file_path = os.path.abspath(args.input_tsv_file_path)
    candidate_transcript_file_path = os.path.abspath(args.candidate_transcript_file_path)
    out_syn_file_path = os.path.abspath(args.out_syn_file_path)

    tsv_file = open(tsv_file_path, "r")
    candidate_transcript_file = open(candidate_transcript_file_path, "r")
    out_syn_file = open(out_syn_file_path, "w")

    # Go through the list of transcripts and store them in a list
    print("Parsing through candidate transcript file")
    candidate_transcript_list = []
    for candidate_transcript in candidate_transcript_file:
        candidate_transcript = candidate_transcript.rstrip()
        if candidate_transcript not in candidate_transcript_list:
            candidate_transcript_list.append(candidate_transcript)
        # If duplicate transcripts are found in the list of transcripts, abort the script
        else:
            sys.exit("Found duplicate entry for " + candidate_transcript)

    # Parse through the Alamut style tsv file
    # Ignore header line
    print("Parsing through tsv file")
    tsv_file_dict = parse_tsv_file(tsv_file)

    print("Number of transcripts in the candidate transcript file is " + str(len(candidate_transcript_list)))
    print("Number of transcripts in the tsv file is " + str(len(tsv_file_dict)))

    # Create the out syn file
    print("Creating output file")
    for candidate_transcript in candidate_transcript_list:
        try:
            candidate_gene = tsv_file_dict[candidate_transcript]
            out_syn_file.write(candidate_gene + "\t" + candidate_transcript + "\n")
        except KeyError:
            print(candidate_transcript + " not found in provided tsv file.")

    tsv_file.close()
    candidate_transcript_file.close()
    out_syn_file.close()


if __name__ == "__main__":
    main()
