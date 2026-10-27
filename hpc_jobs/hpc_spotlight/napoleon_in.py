import pandas as pd
import os
import sys


# Load data
source_biographies = pd.read_csv('data/source_biographies.csv')
napoleon_links = pd.read_csv('data/napoleon_links.csv')
source_names = pd.read_csv('data/napoleon_source_names.csv')   

sys.path.append(os.path.abspath("src"))
from modules.spotlight_weight_source import SpotlightWeightSource

# QID -> title 
titles = dict(zip(source_names["wikidata_id"], source_names["page_title"]))

# Get spotlight weights
source = SpotlightWeightSource()
weights_df = source.assign_weights(
    entities_extracts_missing=source_biographies,
    links_df=napoleon_links,
    title_to_id_map={"en": {"Napoleon": "Q517"}},
)

# Set weight to 1 if the target title is a substring of the source title
def is_substring(row):
    src = titles.get(row["source_wikidata_id"])
    trg = titles.get(row["target_wikidata_id"])
    if not src or not trg:
        return False
    return f" {trg.lower()} " in f" {src.lower()} "

weights_df.loc[weights_df.apply(is_substring, axis=1), "weight"] = 1

weights_df.to_csv('spotlight_weights.csv', index=False)