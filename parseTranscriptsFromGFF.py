####
## Purpose: 
##
## Usage:requires python 2.7.3 
##
## @author JRWalsh 12/13/2018
####

import sys
import argparse
import HTSeq

"""
    Main
"""
def main(args):
    excludedList = parseExcluded(args["exclude"])
    allowedList = parseAllowed(args["allow"])
    parseGFF(args["inputGFF"], excludedList, allowedList)

####
##      Parse a 1 column file of transcript or gene names
####
def parseExcluded(excludeFile):
    if excludeFile == None:
        return None

    with open(excludeFile) as f:
        excludedList = f.readlines()
    excludedList = [x.strip() for x in excludedList]
    return excludedList

####
##      Parse a 1 column file of transcript or gene names
###
def parseAllowed(allowFile):
    if allowFile == None:
        return None

    with open(allowFile) as f:
        allowedList = f.readlines()
    allowedList = [x.strip() for x in allowedList]
    return allowedList

####
##      Loop over the GFF and keep any feature that is a transcript.  It seems that for GRCH37/38 gff files, the features labled as
##      "transcript", "primary_transcript", or anything with "RNA" in the name gives the same results as parsing the fasta file.  
##      These transcripts thus represent "all" transcripts in refSeq. Some errors are expected, ignore them.
####
def parseGFF(gffFile, excludedList, allowedList):
    gff_file = HTSeq.GFF_Reader(gffFile, end_included=True)

    # Loop over the GFF and keep all transcripts.
    transcriptList = list()
    for feature in gff_file:
        if feature.type == "transcript" or feature.type == "primary_transcript" or "RNA" in feature.type:
            transcriptList.append(feature)

    # Now lets get the information we need and only print it if the transcript is in the list of transcripts we need.
    # Errors expected, as some features don't have a transcript_id attribute.
    for feature in transcriptList:
        try:
            transcriptID = feature.attr['transcript_id']
            chrom = feature.iv.chrom
            start = feature.iv.start
            end = feature.iv.end
            strand = feature.iv.strand
            bioType = feature.type
            gene = feature.attr['gene']
            if allowedList is not None:
                if transcriptID in allowedList or gene in allowedList:
                    print('\t'.join(map(str, [transcriptID, chrom, start, end, strand, bioType, gene])))
            elif excludedList is not None:
                if transcriptID not in excludedList and gene not in excludedList:
                    print('\t'.join(map(str, [transcriptID, chrom, start, end, strand, bioType, gene])))
            else:
                print('\t'.join(map(str, [transcriptID, chrom, start, end, strand, bioType, gene])))
        except:
            print "error processing ", feature.name

########################################
# Parse arguments and kick off program #
########################################
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--inputGFF", required=True, help="gff file to parse")
    #ap.add_argument("-o", "--output", required=True, help="output location")
    ap.add_argument("-x", "--exclude", required=False, default=None, help="list of genes or transcripts to exclude from output")
    ap.add_argument("-a", "--allow", required=False, default=None, help="list of genes or transcripts to allow in the output")

    args = vars(ap.parse_args())

    # Cannot set both -x and -a, complain if user tries
    if args["exclude"] and args["allow"]:
        print "Usage: cannot specify both an include and exclude list at the same time"
        sys.exit()

    # What counts as a transcript?
    #args['isTranscript'] = ["transcript", "primary_transcript", "RNA"]

    # What counts as a gene?
    #args['isGene'] = ["gene"]

    # Call main code
    main(args)
