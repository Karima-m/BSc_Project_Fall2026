# Imports
from relik import Relik
from relik.inference.data.objects import RelikOutput
import glob
import os
import pandas as pd

# Parameters
top_ks = [50, 100, 200]
window_sizes = [32, 64, 128]

# folder for results
os.makedirs('results', exist_ok= True)

# Load model
relik = Relik.from_pretrained("sapienzanlp/relik-entity-linking-small", device='cuda')

# Read df with page title and ID 
target_names = pd.read_csv("data/napoleon_target_names.csv")

# Save list with page titles and ID for each target
name_list = target_names['page_title'].values.tolist()
id_list = target_names['wikidata_id'].values.tolist()

# Read Napoleon's biography
with open('data/text_napoleon/Napoleon_en.txt', 'r', encoding='utf-8') as file:
    napoleon_bio = file.read()



# run combinations 
for top_k in top_ks:
    for window_size in window_sizes:

        window_stride = window_size // 2

        # Get relik output
        relik_out: RelikOutput = relik(
            napoleon_bio,
            top_k=top_k,
            window_size=window_size,
            window_stride=window_stride                   
            )

        # Count how many times each target is mentioned
        rows = []

        for name, wikidata_id in zip(name_list, id_list):

            name_count = 0

            for span in relik_out.spans:

                # Add weight if span-label matches a page title
                if span.label == name:
                    name_count += 1

            rows.append({"source_ID": "Q517", "target_ID": wikidata_id, "relik_weight": name_count})

        name_df = pd.DataFrame(rows, columns=["source_ID", "target_ID", "relik_weight"])

        name_df.to_csv(f"results/relik_out_k{top_k}_w{window_size}_s{window_stride}.csv", index=False)