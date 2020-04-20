#!/usr/bin/python3

"""
This script creates the candidate gene list (os.syn) from list of RefSeq and Alamut transcripts
If duplicate transcript numbers exist in two lists, it will chose the transcript and transcript version from Refseq
"""

refseq_file = open("/Users/m006703/test/create_bed_file_test_files/refseq_unique_sorted_transcripts", "r")
alamut_file = open("/Users/m006703/test/create_bed_file_test_files/alamut_uniq_NM_transcripts", "r")
candidate_transcript_file = open("/Users/m006703/test/create_bed_file_test_files/candidate_transcripts", "w")
alamut_only_transcript_file = open("/Users/m006703/test/create_bed_file_test_files/alamut_only_transcripts", "w")


def main():
    refseq_transcripts = {}
    extract_transcripts(refseq_transcripts, refseq_file, "RefSeq")

    alamut_transcript = {}
    extract_transcripts(alamut_transcript, alamut_file, "Alamut")

    count_transcripts(refseq_transcripts, "RefSeq")
    count_transcripts(alamut_transcript, "Alamut")

    candidate_transcripts = {}
    removed_transcripts = {}

    # The RefSeq dictionary must be pruned first in order to keep the RefSeq transcript numbers!!!
    prune_transcript_dictionary(refseq_transcripts, removed_transcripts, candidate_transcripts, "RefSeq")
    count_transcripts(candidate_transcripts, "candidate transcripts after pruning RefSeq")
    count_transcripts(removed_transcripts, "removed transcripts after pruning RefSeq")

    alamut_only_transcripts = prune_transcript_dictionary(alamut_transcript, removed_transcripts,
                                                          candidate_transcripts, "Alamut")
    count_transcripts(candidate_transcripts, "candidate transcripts after pruning Alamut")
    count_transcripts(removed_transcripts, "removed transcripts after pruning Alamut")
    count_transcripts(alamut_only_transcripts, "Alamut only transcripts")

    write_transcripts_to_result_file(candidate_transcripts, candidate_transcript_file)
    write_transcripts_to_result_file(alamut_only_transcripts, alamut_only_transcript_file)

    refseq_file.close()
    alamut_file.close()
    candidate_transcript_file.close()
    alamut_only_transcript_file.close()


def write_transcripts_to_result_file(transcript_dict, transcript_file):
    for transcript_number, transcript_version in transcript_dict.items():
        for version in transcript_version:
            transcript_file.write(transcript_number + "." + version + "\n")


def prune_transcript_dictionary(transcript_dict, removed_transcripts, candidate_transcripts, dict_string):
    """
    Function to keep the most recent version and transcript from the first transcript dictionary
    If duplicate transcript number is present in the second dictionary, the transcript number and versions will be
    sent to the removed_transcript dict
    :param transcript_dict:
    :param removed_transcripts:
    :param candidate_transcripts:
    :param dict_string:
    :return:
    """
    if dict_string == "Alamut":
        alamut_only_transcripts = {}
    for transcript_number, transcript_version_list in transcript_dict.items():
        # Add the transcript number to the candidate transcript dict if it is not present
        if len(transcript_version_list) == 1:
            if transcript_number not in candidate_transcripts.keys():
                candidate_transcripts[transcript_number] = transcript_version_list
                if dict_string == "Alamut":
                    alamut_only_transcripts[transcript_number] = transcript_version_list
            elif transcript_number in candidate_transcripts.keys():
                if transcript_number not in removed_transcripts:
                    removed_transcripts[transcript_number] = transcript_version_list
                else:
                    removed_transcripts[transcript_number] += transcript_version_list
        # If transcript contains multiple version numbers, figure out the most recent version number
        if len(transcript_version_list) >= 2:
            most_recent_version_number = keep_most_recent_version(removed_transcripts, transcript_number,
                                                                  transcript_version_list)
            # If the transcript number is not in the candidate transcripts, add all version
            if transcript_number not in candidate_transcripts.keys():
                candidate_transcripts[transcript_number] = transcript_version_list
                if dict_string == "Alamut":
                    alamut_only_transcripts[transcript_number] = transcript_version_list
            # If the transcript number already exists in candidate transcript,
            # add the most recent version to the already existing transcript number in removed transcripts
            else:
                removed_transcripts[transcript_number].append(most_recent_version_number)
    if dict_string == "Alamut":
        return alamut_only_transcripts


def keep_most_recent_version(transcript_dict, transcript_number, transcript_version_list):
    most_recent_version_number = max(transcript_version_list)
    for version_number in transcript_version_list:
        if version_number != most_recent_version_number:
            if transcript_number not in transcript_dict:
                transcript_dict[transcript_number] = [version_number]
            elif transcript_number in transcript_dict:
                transcript_dict[transcript_number].append(version_number)
    return most_recent_version_number


def count_transcripts(transcript_dict, file_string):
    total_refseq_transcript = 0
    for transcript_number, transcript_version in transcript_dict.items():
        total_refseq_transcript += len(transcript_dict[transcript_number])
    unique_transcript_number = len(transcript_dict.keys())
    print("Number of total transcripts in " + file_string + " " + str(total_refseq_transcript))
    print("Number of unique transcripts in " + file_string + " " + str(unique_transcript_number))


def get_number_from_transcript(transcript_list, transcript_number_list):
    for transcript in transcript_list:
        transcript_number = transcript.split(".")[0]
        transcript_number_list.append(transcript_number)


def extract_transcripts(transcript_dict, transcript_file, file_string):
    for line in transcript_file:
        line = line.rstrip()
        transcript_number = line.split(".")[0]
        transcript_version = line.split(".")[1]
        if transcript_number not in transcript_dict.keys():
            transcript_dict[transcript_number] = []
            transcript_dict[transcript_number].append(transcript_version)
        elif transcript_number in transcript_dict.keys():
            if transcript_version not in transcript_dict[transcript_number]:
                transcript_dict[transcript_number].append(transcript_version)
            else:
                print(transcript_number + "." + transcript_version + " already in dictionary")
                continue


if __name__ == "__main__":
    main()

