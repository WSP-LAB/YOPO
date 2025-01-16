import pandas as pd
import os
import numpy as np
import warnings, sys
import argparse

parser = argparse.ArgumentParser()
args = parser.parse_args()

def customwarn(message, category, filename, lineno, file=None, line=None):
    sys.stdout.write(warnings.formatwarning(message, category, filename, lineno))

BASE_DIR = "/yopo-artifact/data"
BASE_RENDERING_STREAM_DIR = BASE_DIR + "/rendering_stream"
BASE_FEATURE_DIR = BASE_RENDERING_STREAM_DIR + "/modified_features/"

# We drop these domains because comma is included in the url
drop_list = ["www.gazeta.pl", "wyborcza.pl", "www.windy.com"]

print(BASE_FEATURE_DIR)


# handling warnings
warnings.showwarning = customwarn

items = os.listdir(BASE_FEATURE_DIR)
files = [item for item in items if os.path.isfile(os.path.join(BASE_FEATURE_DIR, item))]

merged_df = pd.DataFrame()
total = len(files)
now = 0
for f in files:
    if any(str(f).startswith(drop) for drop in drop_list):
        print("dropping {}".format(f))
        continue

    if now % 1000 == 0:
        print("Now processing [{} / {}]".format(now, total))
    
    f_abs = os.path.join(BASE_FEATURE_DIR, f)
    
    df = pd.read_csv(f_abs, header=None, low_memory=False, on_bad_lines='skip')
    
    merged_df = pd.concat([merged_df, df])
    now += 1

with open("/yopo-artifact/scripts/crawler/adgraph/header_modified_adgraph.txt", 'r') as file:
    headers = file.read().splitlines()[0]

merged_df.columns = headers.split(",")

merged_df.to_csv(BASE_DIR + "/dataset/from_adgraph/modified_features_raw.csv", index=False)