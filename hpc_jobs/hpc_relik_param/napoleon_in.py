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

# Read biographies
text_files = {}

for file_name in glob.glob("data/text_files/*"):

    person = os.path.splitext(os.path.basename(file_name))[0]

    with open(file_name, 'r', encoding='utf-8') as file:
        text_files[person] = file.read()

# run combinations 
for top_k in top_ks:
    for window_size in window_sizes:

        window_stride = window_size // 2

        # Get relik output for each biography
        rows = []

        for name, bio in text_files.items():

            napoleon_count = 0

            relik_out: RelikOutput = relik(
                bio,
                top_k=top_k,
                window_size=window_size,
                window_stride=window_stride
                )

            for span in relik_out.spans:
                #print(span.text, "->", span.label)

                # Only where span-label is Napoleon
                if span.label == 'Napoleon':
                    napoleon_count += 1

            rows.append({'name': name, 'relik_weight': napoleon_count})

        pd.DataFrame(rows).to_csv(f"results/relik_in_k{top_k}_w{window_size}_s{window_stride}.csv", index=False)
