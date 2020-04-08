####
## Purpose: 
##
## Usage: 
##
## @author JRWalsh 12/13/2018
####

import sys
import argparse

"""
    Main
"""
def main(args):
    excludedList = parseExcluded(args["exclude"])
    allowedList = parseAllowed(args["allow"])
    parseAlamut(args["inputAlamutFile"], excludedList, allowedList)

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
##      Main loop 
####
def parseAlamut(alamutFile, excludedList, allowedList):
    with open(alamutFile) as f:
        lines = f.readlines()
        f.close()

    for line in lines:
        try:
            items = line.rstrip().split()
            gene = items[1]
            transcriptID = items[7]
            if allowedList is not None:
                if transcriptID in allowedList or gene in allowedList:
                    print(line.rstrip())
            elif excludedList is not None:
                if transcriptID not in excludedList and gene not in excludedList:
                    print(line.rstrip())
            else:
                print(line.rstrip())
        except:
            if len(line) > 1:
                print "Error in line: ", line

########################################
# Parse arguments and kick off program #
########################################
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--inputAlamutFile", required=True, help="Alamut gene/transcript/exon file to parse")
    #ap.add_argument("-o", "--output", required=True, help="output location")
    ap.add_argument("-x", "--exclude", required=False, default=None, help="list of genes or transcripts to exclude from output")
    ap.add_argument("-a", "--allow", required=False, default=None, help="list of genes or transcripts to allow in the output")

    args = vars(ap.parse_args())

    # Expects txv format with the following columns:
    #['Assembly', 'Symbol', 'HGNC_Id', 'Chromosome', 'Gene_Start', 'Gene_End', 'Strand', 'Transcript', 'Transcript_Start', 'Transcript_End', 'Transcript_CDS_Start', 'Transcript_CDS_End', 'Exon', 'Exon_Start', 'Exon_End', 'Exon_CDS_Start', 'Exon_CDS_End']
    
    # Cannot set both -x and -a, complain if user tries
    if args["exclude"] and args["allow"]:
        print "Usage: cannot specify both an include and exclude list at the same time"
        sys.exit()

    # Call main code
    main(args)
