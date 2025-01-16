import pandas as pd
import os
import numpy as np
import warnings, sys

def customwarn(message, category, filename, lineno, file=None, line=None):
    sys.stdout.write(warnings.formatwarning(message, category, filename, lineno))

BASE_DIR = "/yopo-artifact/data"
BASE_RENDERING_STREAM_DIR = BASE_DIR + "/rendering_stream"
BASE_FEATURE_DIR = BASE_RENDERING_STREAM_DIR + "/features/"

drop_list = [""]

# handling warnings
warnings.showwarning = customwarn

items = os.listdir(BASE_FEATURE_DIR)
files = [item for item in items if os.path.isfile(os.path.join(BASE_FEATURE_DIR, item))]

merged_df = pd.DataFrame()
total = len(files)
now = 0
for f in files:
    # if any(str(f).startswith(drop) for drop in drop_list):
    #     print("dropping {}".format(f))
    #     continue

    if now % 1000 == 0:
        print("Now processing [{} / {}]".format(now, total))
    
    f_abs = os.path.join(BASE_FEATURE_DIR, f)
    try:
        df = pd.read_csv(f_abs, header=None, low_memory=False)
    except:
        print("Error in {}".format(f_abs))
    
    # if the number of network requests is fewer than 2, we assume it to be incorrect data.
    if df.shape[0] < 3:
        now += 1
        continue
    merged_df = pd.concat([merged_df, df])
    now += 1

merged_df.to_csv(BASE_DIR + "/dataset/from_adgraph/features_raw.csv", index=False)