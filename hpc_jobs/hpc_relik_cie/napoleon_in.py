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

#print('INCOMING EDGES')

for name, bio in text_files.items():

    napoleon_count = 0

    relik_out: RelikOutput = relik(bio)

    for span in relik_out.spans:
        
        #print(span.text, "->", span.label)

        if span.label == 'Napoleon':
            napoleon_count += 1

    rows.append({'name': name, 'relik_cie_weight': napoleon_count})

    pd.DataFrame(rows).to_csv("relik_cie_weights.csv", index=False)
