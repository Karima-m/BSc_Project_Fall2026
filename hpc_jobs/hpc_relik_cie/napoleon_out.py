# Imports
from relik import Relik
from relik.inference.data.objects import RelikOutput
import glob
import os
import pandas as pd
import re


# Load model
relik = Relik.from_pretrained("relik-ie/relik-cie-small", device='cuda')

# Read df with page title and ID 
target_names = pd.read_csv("data/napoleon_target_names.csv")

# Save list with page titles and ID for each target
name_list = target_names['page_title'].values.tolist()
id_list = target_names['wikidata_id'].values.tolist()

# Make pattern for identifaction of wikipedia title vs Relik's labels
# registers hyphens and spaces 
SEP = r'[\s\-‐–]+' 

# makes case insensitive and allow optional ending  
patterns = [re.compile(SEP.join(re.escape(word) for word in re.split(SEP, name.strip()))
                       + r'(?: of [A-Z][\w\-]*)?',
                       re.IGNORECASE)
            for name in name_list]

# Read Napoleon's biography
with open('data/text_napoleon/Napoleon_en.txt', 'r') as file:
    napoleon_bio = file.read()

# Get relik output
relik_out: RelikOutput = relik(napoleon_bio)

# Count how many times each target is mentioned
rows = []

for pattern, wikidata_id in zip(patterns, id_list):

    name_count = 0

    for span in relik_out.spans:

        #print(span.text, "->", span.label)

        # Add weight if page title and span label are the same or title "... of ..."
        if pattern.fullmatch(span.label):
            name_count += 1

    rows.append({"source_ID": "Q517", "target_ID": wikidata_id, "relik_cie_weight": name_count})

name_df = pd.DataFrame(rows, columns=["source_ID", "target_ID", "relik_cie_weight"])

name_df.to_csv('relik_cie_napoleon_weights.csv', index=False)