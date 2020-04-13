#!/usr/bin/python3

import sys

syn_file_transcript_only = open("/Users/m006703/test/create_bed_file_test_files/os.syn.tmp2", "r")
syn_file_with_gene = open("/Users/m006703/test/create_bed_file_test_files/os.syn.tmp2_new", "r")

transcript_only_transcripts = []
for line in syn_file_transcript_only:
    line = line.rstrip()
    if line not in transcript_only_transcripts:
        transcript_only_transcripts.append(line)
    else:
        sys.exit("Found duplicate transcript in transcript only file " + line)

transcript_gene_dict = {}
for line in syn_file_with_gene:
    line = line.rstrip()
    line_item = line.split("\t")
    gene = line_item[0]
    transcript = line_item[1]
    if transcript not in transcript_gene_dict.keys():
        transcript_gene_dict[transcript] = gene
    else:
        sys.exit("Found duplicate transcript in gene transcript file: " + transcript)

for key in transcript_gene_dict.keys():
    if key not in transcript_only_transcripts:
        print(key + " is not in transcript only file and is associated with gene " +
              transcript_gene_dict[key])

syn_file_transcript_only.close()
syn_file_with_gene.close()
