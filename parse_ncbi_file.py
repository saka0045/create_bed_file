#!/usr/bin/python3

ncbi_file = open("/Users/m006703/test/create_bed_file_test_files/nuccore_result.txt", "r")
parsed_ncbi_file = open("/Users/m006703/test/create_bed_file_test_files/parsed_ncbi_result_file", "w")

# Ignore the first blank line
ncbi_file.readline()

n = 1
ncbi_dict = {}
while n in range(1, 310):
    for line in ncbi_file:
        line = line.rstrip()
        if line.startswith(str(n) + "."):
            # print(line)
            ncbi_file.readline()
            third_line = ncbi_file.readline().rstrip()
            if third_line.startswith("NM_"):
                transcript = third_line.split(" ")[0]
                result = "Valid RefSeq transcript"
                ncbi_dict[transcript] = result
                # print(third_line)
                # print(transcript)
            else:
                result = third_line
                fourth_line = ncbi_file.readline().rstrip()
                transcript = fourth_line.split(" ")[0]
                ncbi_dict[transcript] = result
                # print(fourth_line)
                # print(transcript)
            n += 1
        else:
            continue

for transcript, result in ncbi_dict.items():
    parsed_ncbi_file.write(transcript + "\t" + result + "\n")

ncbi_file.close()
parsed_ncbi_file.close()
