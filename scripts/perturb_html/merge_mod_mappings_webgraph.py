import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--map-idx', type=int)
args = parser.parse_args()


# Read the CSV files
a_df = pd.read_csv('/yopo-artifact/data/rendering_stream/mod_mappings_webgraph/merged/url_mappings.csv', header=None)
b_df = pd.read_csv('/yopo-artifact/data/rendering_stream/mod_mappings_webgraph/map_mod_{}.csv'.format(args.map_idx), header=None)

# Concatenate the two dataframes
result_df = pd.concat([a_df, b_df], axis=0)

# Save the concatenated dataframe to a new CSV file
result_df.to_csv('/yopo-artifact/data/rendering_stream/mod_mappings_webgraph/merged/merged_map_mod_{}.csv'.format(args.map_idx), index=False)
