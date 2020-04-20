#!/usr/bin/python3

refseq_file = open("/Users/m006703/test/create_bed_file_test_files/refseq_unique_sorted_transcripts", "r")
alamut_file = open("/Users/m006703/test/create_bed_file_test_files/alamut_uniq_NM_transcripts", "r")
original_not_in_refseq = open("/Users/m006703/test/create_bed_file_test_files/original_not_in_refseq", "w")


def main():
    refseq_transcripts = []
    extract_transcripts(refseq_transcripts, refseq_file, "RefSeq")

    alamut_transcript = []
    extract_transcripts(alamut_transcript, alamut_file, "Alamut")

    print("Total number of unique transcript in RefSeq: " + str(len(refseq_transcripts)))
    print("Total number of unique transcripts in Alamut: " + str(len(alamut_transcript)))

    only_in_alamut = []
    for transcript in alamut_transcript:
        if transcript not in refseq_transcripts:
            only_in_alamut.append(transcript)
    print("Number of NM transcripts only in Alamut file: " + str(len(only_in_alamut)))

    refseq_transcript_dict = {}
    get_number_from_transcript(refseq_transcripts, refseq_transcript_dict)

    only_in_alamut_transcript_dict = {}
    get_number_from_transcript(only_in_alamut, only_in_alamut_transcript_dict)

    count_transcripts(refseq_transcript_dict, "RefSeq")
    count_transcripts(only_in_alamut_transcript_dict, "Only in Alamut")

    completely_not_in_refseq_dict = {}
    for transcript_number, transcript_version in only_in_alamut_transcript_dict.items():
        if transcript_number not in refseq_transcript_dict.keys():
            completely_not_in_refseq_dict[transcript_number] = transcript_version
            if len(transcript_version) >= 2:
                for version in transcript_version:
                    print(transcript_number + "." + version)

    count_transcripts(completely_not_in_refseq_dict, "Completely not in RefSeq")

    """
    different_version_transcripts = []
    completely_not_in_refseq = []
    for transcript_number in only_in_alamut_transcript_dict:
        if transcript_number in refseq_transcript_dict:
            different_version_transcripts.append(transcript_number)
        else:
            completely_not_in_refseq.append(transcript_number)

    for transcript in completely_not_in_refseq:
        original_not_in_refseq.write(transcript + "\n")

    print("Number of shared transcripts with different versions: " + str(len(different_version_transcripts)))
    print("Number of transcripts that are not represented in RefSeq at all: " + str(len(completely_not_in_refseq)))
    """

    refseq_file.close()
    alamut_file.close()
    original_not_in_refseq.close()


def count_transcripts(transcript_dict, file_string):
    total_refseq_transcript = 0
    for transcript_number, transcript_version in transcript_dict.items():
        total_refseq_transcript += len(transcript_dict[transcript_number])
    unique_transcript_number = len(transcript_dict.keys())
    print("Number of total transcripts in " + file_string + " " + str(total_refseq_transcript))
    print("Number of unique transcripts in " + file_string + " " + str(unique_transcript_number))


def get_number_from_transcript(transcript_list, transcript_dict):
    for transcript in transcript_list:
        transcript_number = transcript.split(".")[0]
        transcript_version = transcript.split(".")[1]
        if transcript_number not in transcript_dict.keys():
            transcript_dict[transcript_number] = []
            transcript_dict[transcript_number].append(transcript_version)
        elif transcript_number in transcript_dict.keys():
            if transcript_version not in transcript_dict[transcript_number]:
                transcript_dict[transcript_number].append(transcript_version)
            else:
                print(transcript_number + "." + transcript_version + " already in dictionary")
                continue


def extract_transcripts(transcript_list, transcript_file, file_string):
    for line in transcript_file:
        line = line.rstrip()
        transcript_list.append(line)


if __name__ == "__main__":
    main()
