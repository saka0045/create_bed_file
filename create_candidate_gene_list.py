#!/usr/bin/python3

refseq_file = open("/Users/m006703/test/create_bed_file_test_files/refseq_unique_sorted_transcripts", "r")
alamut_file = open("/Users/m006703/test/create_bed_file_test_files/alamut_uniq_NM_transcripts", "r")


def main():
    refseq_transcripts = {}
    extract_transcripts(refseq_transcripts, refseq_file, "RefSeq")

    alamut_transcript = {}
    extract_transcripts(alamut_transcript, alamut_file, "Alamut")

    refseq_total_transcripts, refseq_unique_transcripts = count_transcripts(refseq_transcripts)
    alamut_total_transcripts, alamut_unique_transcript = count_transcripts(alamut_transcript)

    print("Number of total transcripts in RefSeq file: " + str(refseq_total_transcripts))
    print("Number of unique transcript in RefSeq file: " + str(refseq_unique_transcripts))
    print("Number of total transcripts in Alamut file: " + str(alamut_total_transcripts))
    print("Number of unique transcripts in Alamut file: " + str(alamut_unique_transcript))

    only_in_alamut = []
    for transcript in alamut_transcript:
        if transcript not in refseq_transcripts:
            only_in_alamut.append(transcript)
    print("Number of NM transcripts only in Alamut file: " + str(len(only_in_alamut)))

    refseq_nm_transcripts_number_only = []
    get_number_from_transcript(refseq_transcripts, refseq_nm_transcripts_number_only)

    only_in_alamut_nm_transcript_number_only = []
    get_number_from_transcript(only_in_alamut, only_in_alamut_nm_transcript_number_only)

    different_version_transcripts = []
    completely_not_in_refseq = []
    for transcript_number in only_in_alamut_nm_transcript_number_only:
        if transcript_number in refseq_nm_transcripts_number_only:
            different_version_transcripts.append(transcript_number)
        else:
            completely_not_in_refseq.append(transcript_number)

    print("Number of shared transcripts with different versions: " + str(len(different_version_transcripts)))
    print("Number of transcripts that are not represented in RefSeq at all: " + str(len(completely_not_in_refseq)))

    refseq_file.close()
    alamut_file.close()


def count_transcripts(transcript_dict):
    total_refseq_transcript = 0
    for transcript_number, transcript_version in transcript_dict.items():
        total_refseq_transcript += len(transcript_dict[transcript_number])
    unique_transcript_number = len(transcript_dict.keys())
    return total_refseq_transcript, unique_transcript_number


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

