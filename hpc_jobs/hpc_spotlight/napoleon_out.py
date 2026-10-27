# Imports
import pandas as pd
import os
import sys

sys.path.append(os.path.abspath("src"))
from modules.spotlight_weight_source import SpotlightWeightSource


# Load data
napoleon_biography = pd.read_csv('data/napoleon_out/napoleon_biography.csv')
napoleon_out_links = pd.read_csv('data/napoleon_out/napoleon_out_links.csv')
target_names = pd.read_csv('data/napoleon_out/napoleon_target_names.csv')  

# Title -> QID
title_to_id_map = {"en": dict(zip(target_names["page_title"], target_names["wikidata_id"]))}

# Get spotlight weights
source = SpotlightWeightSource()
weights_df = source.assign_weights(
    entities_extracts_missing=napoleon_biography,
    links_df=napoleon_out_links,
    title_to_id_map=title_to_id_map
)

weights_df.to_csv('spotlight_napoleon_weights.csv', index=False)