#!/usr/bin/env python

import gffutils

# Only need to make the DB once, takes a long time
db = gffutils.create_db("/dlmp/sandbox/cgslIS/Yuta/Illumina/hg38_bed_file/raw_data/GRCh38_latest_genomic.gff.gz",
                        dbfn='GRCh38_unsorted.db', id_spec=["ID", "Name"], force=True, keep_order=False,
                        merge_strategy='create_unique', sort_attribute_values=False)

print("script finished")
