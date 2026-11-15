# Imports
from relik import Relik
from relik.inference.data.objects import RelikOutput
import glob
import os
import pandas as pd
import re


relik = Relik.from_pretrained("sapienzanlp/relik-entity-linking-base", device='cuda')

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
with open('data/text_napoleon/Napoleon_en.txt', 'r', encoding='utf-8') as file:
    napoleon_bio = file.read()

relik_out: RelikOutput = relik(napoleon_bio)

#save every span relik found 
spans_df = pd.DataFrame([(s.text, s.label) for s in relik_out.spans], columns=["span_text", "label"])
spans_df.to_csv("relik_out_base_spans.csv", index=False)


# Count how many times each target is mentioned
rows = []

for pattern, wikidata_id in zip(patterns, id_list):

    name_count = 0

    for span in relik_out.spans:

        # Add weight if page title and span label are the same or title "... of ..."
        if pattern.fullmatch(span.label):
            name_count += 1

    rows.append({"source_ID": "Q517", "target_ID": wikidata_id, "relik_weight": name_count})

name_df = pd.DataFrame(rows, columns=["source_ID", "target_ID", "relik_weight"])
name_df.to_csv("relik_out_base_spans.csv", index=False)