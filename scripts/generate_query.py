import os 
import pandas as pd 
import numpy as np
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, make_scorer
from sklearn.utils import resample
from joblib import dump, load
import pickle
import feature_names_adgraph, feature_names_webgraph, feature_names_adflush, feature_names_pagegraph
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--csv-path', type=str)
parser.add_argument('--csv-name', type=str)
parser.add_argument('--nn-csv-name', type=str)
parser.add_argument('--model-fpath', type=str)
parser.add_argument('--perc', type=str)
parser.add_argument('--query-size', type=str)
parser.add_argument('--mode', type=str)
args = parser.parse_args()

mode = args.mode

#load model
with open(args.csv_path + args.model_fpath, 'rb') as f:
    clf = pickle.load(f)

# SELECT QUERIES
query_size = args.query_size
data = pd.read_csv(args.csv_path + args.csv_name)
nn_csv = pd.read_csv(args.csv_path + args.nn_csv_name)

# shuffle
perm = np.random.permutation(len(data))
data = data.iloc[perm].reset_index(drop=True)
nn_csv = nn_csv.iloc[perm].reset_index(drop=True)

if mode == "webgraph":
    X = data.drop(["CLASS"] + feature_names_webgraph.FEATURES_TO_EXCLUDE_WEBGRAPH, axis=1)
    y = data["CLASS"]
    X_NN = nn_csv.drop(["CLASS"], axis=1)
elif mode == "adgraph":
    X = data.drop(["CLASS"] + feature_names_adgraph.FEATURES_TO_EXCLUDE_ADGRAPH, axis=1)
    y = data["CLASS"]
    X_NN = nn_csv.drop(["CLASS"], axis=1)
elif mode == "adflush":
    X = data.drop(["CLASS"] + feature_names_adflush.FEATURES_TO_EXCLUDE_ADFLUSH, axis=1)
    y = data["CLASS"]
    X_NN = nn_csv.drop(["CLASS"], axis=1)
elif mode == "pagegraph":
    X = data.drop(["CLASS"] + feature_names_pagegraph.FEATURES_TO_EXCLUDE_PAGEGRAPH, axis=1)
    y = data["CLASS"]
    X_NN = nn_csv.drop(["CLASS"], axis=1)
else:
    raise("Unkown mode")

y_result = clf.predict(X)
y_result = pd.DataFrame(y_result, columns=["CLASS"])
y_label = pd.DataFrame(y, columns=["CLASS"])
query_concat = pd.concat([X_NN, y_result], axis=1)
inversion_concat = pd.concat([X_NN, y_label], axis=1)

query_concat.to_csv("/yopo-artifact/data/dataset/temp_{}_for_surrogate_{}.csv".format(args.perc, mode), index=False)
inversion_concat.to_csv("/yopo-artifact/data/dataset/temp_{}_for_inversion_{}.csv".format(args.perc, mode), index=False)

# save temp
selected_query = pd.read_csv(args.csv_path + "../temp_{}_for_surrogate_{}.csv".format(args.perc, mode))
remaining_queries = pd.read_csv(args.csv_path + "../temp_{}_for_inversion_{}.csv".format(args.perc, mode))

# Select random N queries
selected_query = selected_query.sample(n=int(query_size))

# save
if mode == "webgraph":
    selected_query_drop = selected_query.drop(feature_names_webgraph.FEATURES_TO_EXCLUDE_WEBGRAPH, axis=1)
elif mode == "adgraph":
    selected_query_drop = selected_query.drop(feature_names_adgraph.FEATURES_TO_EXCLUDE_ADGRAPH, axis=1)
elif mode == "adflush":
    selected_query_drop = selected_query.drop(feature_names_adflush.FEATURES_TO_EXCLUDE_ADFLUSH, axis=1)
elif mode == "pagegraph":
    selected_query_drop = selected_query.drop(feature_names_pagegraph.FEATURES_TO_EXCLUDE_PAGEGRAPH, axis=1)
else:
    raise("Unkown adblocker!")

selected_query_drop = selected_query_drop.astype(float)
selected_query_drop.to_csv("/yopo-artifact/data/dataset/for_surrogate/final_query_{}perc_{}_{}.csv".format(args.perc, query_size, mode), index=False)

print("  Surrogate model dataset size : {}".format(selected_query.shape[0]))

# save remaining query
selected_indices = selected_query.index
nn_csv = nn_csv.drop(selected_indices)
nn_csv = nn_csv[nn_csv["CLASS"] == 1]

if mode == "webgraph":
    nn_csv_drop = nn_csv.drop(feature_names_webgraph.FEATURES_TO_EXCLUDE_WEBGRAPH, axis=1)
elif mode == "adgraph":
    nn_csv_drop = nn_csv.drop(feature_names_adgraph.FEATURES_TO_EXCLUDE_ADGRAPH, axis=1)
elif mode == "adflush":
    nn_csv_drop = nn_csv.drop(feature_names_adflush.FEATURES_TO_EXCLUDE_ADFLUSH, axis=1) 
elif mode == "pagegraph":
    nn_csv_drop = nn_csv.drop(feature_names_pagegraph.FEATURES_TO_EXCLUDE_PAGEGRAPH, axis=1)
else:
    raise("Unkown adblocker!")

nn_csv_drop = nn_csv_drop.astype(float)
nn_csv_drop.to_csv("/yopo-artifact/data/dataset/final_{}perc_{}_for_inversion_{}.csv".format(args.perc, query_size, mode), index=False)

print("  Done.")