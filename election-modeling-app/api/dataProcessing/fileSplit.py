import dask.dataframe as dd
import pandas as pd
import os

abbreviations = [
    "AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "IA",
    "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO",
    "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI",
    "WV", "WY", "DC"
]

import csv

with open('electionData/2016-precinct-state.csv', encoding='latin-1') as fin:    
    csvin = csv.DictReader(fin)
    # Category -> open file lookup
    outputs = {}
    for row in csvin:
        cat = row['state_postal']
        # Open a new file and write the header
        if cat not in outputs:
            os.makedirs('electionData/{}/results/'.format(cat), exist_ok=True)
            fout = open('electionData/{}/results/{}_2016.csv'.format(cat, cat), 'w')
            dw = csv.DictWriter(fout, fieldnames=csvin.fieldnames)
            dw.writeheader()
            outputs[cat] = fout, dw
        # Always write the row
        outputs[cat][1].writerow(row)
    # Close all the files
    for fout, _ in outputs.values():
        fout.close()