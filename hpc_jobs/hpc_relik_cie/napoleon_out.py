from relik import Relik
from relik.inference.data.objects import RelikOutput
import glob
import os
import pandas as pd

relik = Relik.from_pretrained("relik-ie/relik-cie-small", device='cuda')

target_names = pd.read_csv("data/napoleon_target_names.csv")

name_list = target_names['page_title'].values.tolist()
id_list = target_names['wikidata_id'].values.tolist()

# Read Napoleon's biography
with open('data/text_napoleon/Napoleon_en.txt', 'r') as file:
    napoleon_bio = file.read()

relik_out: RelikOutput = relik(napoleon_bio)

# Count how many times each target is mentioned
rows = []

#print('OUTGOING EDGES')

for name, wikidata_id in zip(name_list, id_list):

    name_count = 0

    for span in relik_out.spans:

        #print(span.text, "->", span.label)

        if span.label == name:
            name_count += 1

    rows.append({"source_ID": "Q517", "target_ID": wikidata_id, "relik_cie_weight": name_count})

name_df = pd.DataFrame(rows, columns=["source_ID", "target_ID", "relik_cie_weight"])

name_df.to_csv('relik_cie_napoleon_weights.csv', index=False)