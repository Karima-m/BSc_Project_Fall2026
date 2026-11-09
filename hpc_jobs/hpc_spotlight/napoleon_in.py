# Imports
import pandas as pd
import os
import sys

sys.path.append(os.path.abspath("src"))
from modules.spotlight_weight_source import SpotlightWeightSource


# Load data
source_biographies = pd.read_csv('data/source_biographies.csv')
napoleon_links = pd.read_csv('data/napoleon_links.csv')


# Get spotlight weights
source = SpotlightWeightSource()
weights_df = source.assign_weights(
    entities_extracts_missing=source_biographies,
    links_df=napoleon_links,
    title_to_id_map={"en": {"Napoleon": "Q517"}},
)

weights_df = weights_df.rename(columns={
    "source_wikidata_id": "source_ID",
    "target_wikidata_id": "target_ID",
    "weight": "spotlight_weight",
})

weights_df.to_csv('spotlight_weights.csv', index=False)
