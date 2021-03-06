#!/usr/bin/python3

"""
This script removes the Y mapping of transcripts that were identified in XY_mapped_transcripts
The refseq_alamut.tsv and XY_mapped_transcripts file needs to be created in advance
"""

import argparse
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r", "--refseqAlamutFile", dest="refseq_alamut_file_path", required=True,
        help="Path to the refseq_alamut.tsv file"
    )
    parser.add_argument(
        "-c", "--completeAlamuteFile", dest="complete_refseq_alamut_file_path", required=True,
        help="Path, including the name, of the result file to output"
    )
    parser.add_argument(
        "-x", "--xyMappedTranscriptsFile", dest="xy_mapped_transcripts_file_path", required=True,
        help="Path to the XY_mapped_transcripts file"
    )

    args = parser.parse_args()

    refseq_alamut_file_path = os.path.abspath(args.refseq_alamut_file_path)
    complete_refseq_alamut_file_path = os.path.abspath(args.complete_refseq_alamut_file_path)
    xy_mapped_transcripts_file_path = os.path.abspath(args.xy_mapped_transcripts_file_path)

    refseq_alamut_file = open(refseq_alamut_file_path, "r")
    complete_refseq_alamut_file = open(complete_refseq_alamut_file_path, "w")
    xy_mapped_transcripts_file = open(xy_mapped_transcripts_file_path, "r")

    # Parse through the XY_mapped_transcripts file
    xy_mapped_transcripts = []
    for xy_transcript in xy_mapped_transcripts_file:
        xy_transcript = xy_transcript.rstrip()
        xy_mapped_transcripts.append(xy_transcript)

    # Go through the refseq_alamut file and remove the Y mapping from the list of transcripts in xy_mapped_transcripts
    # Keep track of the transcripts that were removed
    deleted_y_transcript = []
    for line in refseq_alamut_file:
        line = line.rstrip()
        line_item = line.split("\t")
        chromosome = line_item[3]
        if chromosome == "Y":
            transcript = line_item[7]
            exon = line_item[12]
            if transcript in xy_mapped_transcripts:
                print("Removing " + transcript + " from chromosome " + chromosome + " exon " + exon)
                if transcript not in deleted_y_transcript:
                    deleted_y_transcript.append(transcript)
            else:
                complete_refseq_alamut_file.write(line + "\n")
        else:
            complete_refseq_alamut_file.write(line + "\n")

    print("Deleted the following transcripts:")
    print("\n".join(deleted_y_transcript))
    print("Total number of deleted Y transcripts: " + str(len(deleted_y_transcript)))

    refseq_alamut_file.close()
    complete_refseq_alamut_file.close()
    xy_mapped_transcripts_file.close()


if __name__ == "__main__":
    main()
