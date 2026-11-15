# Imports
from relik import Relik
from relik.inference.data.objects import RelikOutput
import glob
import os
import pandas as pd

relik = Relik.from_pretrained("relik-ie/relik-cie-small", device='cuda')

# Read biographies
text_files = {}

for file_name in glob.glob("data/text_files/*"):

    person = os.path.splitext(os.path.basename(file_name))[0]

    with open(file_name, 'r', encoding='utf-8') as file:
        text_files[person] = file.read()


rows = []
all_spans = []
 
for name, bio in text_files.items():
 
    napoleon_count = 0
 
    relik_out: RelikOutput = relik(bio)
 
    for span in relik_out.spans:
 
        # save every span relik found
        all_spans.append({'person': name, 'span_text': span.text, 'label': span.label})
 
        # Only where span-label is Napoleon
        if span.label == 'Napoleon':
            napoleon_count += 1
 
    rows.append({'name': name, 'relik_weight': napoleon_count})
 
pd.DataFrame(rows).to_csv("relik_in.csv", index=False)
pd.DataFrame(all_spans).to_csv("relik_in_cie_spans.csv", index=False)
