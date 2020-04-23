#!/usr/bin/python3

"""
Takes the summary text file from NCBI after searching for lists of transcripts and parse the result out
"""

import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--inputNcbiFile", dest="input_ncbi_file_path", required=True,
    )
    parser.add_argument(
        "-o", "--outDir", dest="output_directory", required=True,
        help="OUtput directory to save the parsed result file"
    )
    parser.add_argument(
        "-n", "--numberOfResults", dest="number_of_results",required=True,
        help="Number of results returned by NCBI"
    )
    parser.add_argument(
        "-t", "--tsvFile", dest="tsv_file_path", required=True,
        help="Combined RefSeq and Alamut tsv file, in Alamut style"
    )

    args = parser.parse_args()

    ncbi_file_path = os.path.abspath(args.input_ncbi_file_path)
    out_dir = os.path.abspath(args.output_directory)
    tsv_file_path = os.path.abspath(args.tsv_file_path)

    ncbi_file = open(ncbi_file_path, "r")
    parsed_ncbi_file = open(out_dir + "/parsed_ncbi_result_file", "w")
    number_of_results = int(args.number_of_results)
    tsv_file = open(tsv_file_path, "r")

    # Ignore the first blank line
    ncbi_file.readline()

    ncbi_dict = extract_ncbi_results(number_of_results, ncbi_file)

    print("You have requested " + str(number_of_results) + " results from NCBI summary file")
    number_of_transcripts_parsed = len(ncbi_dict.keys())
    if number_of_results == number_of_transcripts_parsed:
        print("The script successfully parsed " + str(number_of_transcripts_parsed) + " transcripts")
    else:
        print("Something went wrong, only " + str(number_of_transcripts_parsed) + " was parsed")
        sys.exit("Aborting script")

    # Parse through the Alamut style tsv file
    tsv_file_dict = parse_tsv_file(tsv_file)

    # Write results to result file
    parsed_ncbi_file.write("Transcript\tGene\tResult\n")
    for transcript, result in ncbi_dict.items():
        try:
            gene = tsv_file_dict[transcript]
        except KeyError:
            sys.exit("Transcript: " + transcript + " is not found in the tsv file")
        parsed_ncbi_file.write(transcript + "\t" + gene + "\t" + result + "\n")

    ncbi_file.close()
    parsed_ncbi_file.close()
    tsv_file.close()


def parse_tsv_file(tsv_file):
    """
    Parse through the RefSeq Alamut tsv file and extract the transcript and gene
    :param tsv_file:
    :return:
    """
    # Ignore header line
    tsv_file.readline()
    tsv_file_dict = {}
    for line in tsv_file:
        line = line.rstrip()
        tsv_line_item = line.split("\t")
        tsv_gene = tsv_line_item[1]
        tsv_transcript = tsv_line_item[7]
        if tsv_transcript not in tsv_file_dict.keys():
            tsv_file_dict[tsv_transcript] = tsv_gene
    return tsv_file_dict


def extract_ncbi_results(number_of_results, ncbi_file):
    """
    Parse the NCBI summary text file
    :param number_of_results:
    :param ncbi_file:
    :return:
    """
    n = 1
    ncbi_dict = {}
    # Change the range depending on how many results is returned
    while n in range(1, number_of_results):
        for line in ncbi_file:
            line = line.rstrip()
            # Each entry starts with int.)
            if line.startswith(str(n) + "."):
                # print(line)
                # Skip the next (second) line for the entry
                ncbi_file.readline()
                third_line = ncbi_file.readline().rstrip()
                # If the transcript is valid, the third line would have the NM transcript number
                if third_line.startswith("NM_"):
                    transcript = third_line.split(" ")[0]
                    result = "Valid RefSeq transcript"
                    ncbi_dict[transcript] = result
                    # print(third_line)
                    # print(transcript)
                else:
                    # If the transcript is no longer available in RefSeq, the third line will have an explanation
                    result = third_line
                    # Fourth line in this case has the NM transcript number
                    fourth_line = ncbi_file.readline().rstrip()
                    transcript = fourth_line.split(" ")[0]
                    ncbi_dict[transcript] = result
                    # print(fourth_line)
                    # print(transcript)
                n += 1
            else:
                continue
    return ncbi_dict


if __name__ == "__main__":
    main()
