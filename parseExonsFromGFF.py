"""
Purpose: 

Usage:  Must have a the gff and refSeq_not_cava files in this directory.  Should pipe output through an "grep -v error"
        filter before pipeing to output file.

@author JRWalsh 10/02/2018
"""
import re

## Installed locally
import sys, os
sys.path.append (os.environ['HOME'] + 'python/lib/python')
import gffutils

## Only need to make the DB once, takes a long time
#db = gffutils.create_db("GRCh37_latest_genomic.gff.gz", dbfn='GRCh37_unsorted.db', id_spec=["ID", "Name"], force=True, keep_order=False, merge_strategy='create_unique', sort_attribute_values=False)

## Read existing gffutils db, created above
db = gffutils.FeatureDB('/dlmp/sandbox/cgslIS/jrwalsh/git/local/parseGFF/tempData/GRCh37_unsorted.db', keep_order=True)

# This file acts as an "allowed-list" filter. We will only keep transcripts in this list.
with open("/dlmp/sandbox/cgslIS/jrwalsh/git/local/parseGFF/tempData/NM_transcripts_in_refseq_not_alamut") as f:
    allowedList = f.readlines()
allowedList = [x.strip() for x in allowedList]

# Track how many things in the allowedList we actually find
foundSet = set()

# We are reconstructing the format of the downloaded_alamut.tsv file.  We will create new lines using only transcripts from the allowedList.
# Format: Assembly        Symbol  HGNC_Id Chromosome      Gene_Start      Gene_End        Strand  Transcript      Transcript_Start        Transcript_End  Transcript_CDS_Start    Transcript_CDS_End      Exon    Exon_Start      Exon_End        Exon_CDS_Start  Exon_CDS_End
# Errors expected, as some features don't have certain attributes like name or transcript_id.  Just skip these.
for gene in db.all_features(featuretype='gene'):
    geneName = gene['Name'][0]
    geneStart = gene.start
    geneEnd = gene.end
    strand = gene.strand
    if strand == "+": # Convert format from +/- to 1/-1
        strand = "1"
    if strand == "-":
        strand = "-1" 
    chromosome = gene.seqid
    if chromosome.startswith("NC_"):
        chromosome = re.split('_|\.', re.sub("00000|0000","",chromosome))[1] # Convert format from "NC_000001.10" to "1"
        if chromosome == "23": # Convert chromosomes 23/24 to X/Y
            chromosome = "X"
        elif chromosome == "24":
            chromosome = "Y"
    elif chromosome.startswith("NW_") or chromosome.startswith("NT_") or chromosome.startswith("M"):
        continue
    Dbxref = gene.attributes['Dbxref']
    try:
        for item in Dbxref:
            if "HGNC" in item:
                HGNC = item.split(":")[-1]
    except:
        HGNC = "-"
    #print geneName, geneStart, geneEnd
    for transcript in db.children(gene, level=1):
        try:
            transcriptName = transcript['Name'][0]
            transcriptStart = transcript.start
            transcriptEnd = transcript.end
            transcriptCDSStart = 0
            transcriptCDSEnd = 0
            #print transcriptName, transcriptStart, transcriptEnd
            try:
                transcriptCDSStart = next(db.children(transcript, featuretype='CDS', order_by='start')).start
                transcriptCDSEnd = next(db.children(transcript, featuretype='CDS', order_by='start', reverse=True)).end
            except:
                transcriptCDSStart = -1
                transcriptCDSEnd = -1
            if True: #transcriptName in allowedList: #filter here if needed
                i = 1
                reverse = False
                if strand == "-1" or strand == "-":
                    reverse = True
                for exon in db.children(transcript, featuretype='exon', order_by='start', reverse=reverse):
                    exonNumber = i
                    i = i+1
                    exonStart = exon.start
                    exonEnd = exon.end
                    #print exonNumber, exonStart, exonEnd
                    cdsStart = "0" # These will be 0 if there is no matching cds or -1 if there are no cds at all
                    cdsEnd = "0"
                    try:
                        for cds in db.children(transcript, featuretype='CDS', order_by='start', reverse=reverse):
                            if cds.start == exonStart or cds.end == exonEnd:
                                cdsStart = cds.start
                                cdsEnd = cds.end
                                break
                            elif exonStart < cds.start and cds.end < exonEnd: # Edge case where CDS is wholly contained in exactly 1 exon, so neither cds start nor end match exon start/end
                                cdsStart = cds.start
                                cdsEnd = cds.end
                                break
                    except:
                        cdsStart = "-1"
                        cdsEnd = "-1"
                    print('\t'.join(map(str, ["GRCh37.p13", geneName, HGNC, chromosome, geneStart, geneEnd, strand, transcriptName, transcriptStart, transcriptEnd, transcriptCDSStart, transcriptCDSEnd, exonNumber, exonStart, exonEnd, cdsStart, cdsEnd])))
                    foundSet.add(transcriptName)
        except:
            continue
