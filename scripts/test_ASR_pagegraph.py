import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import argparse
import joblib
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--csv-path', type=str)
parser.add_argument('--csv-name-final', type=str)
parser.add_argument('--csv-name-before-attack', type=str)
parser.add_argument('--model-fpath', type=str)
parser.add_argument('--attack-option', type=str)
args = parser.parse_args()

with open(args.model_fpath, 'rb') as file:
    clf = pickle.load(file)

csv_path = args.csv_path
csv_name_before_attack = args.csv_name_before_attack
csv_name_final = args.csv_name_final
attack_option = args.attack_option

data_ad = pd.read_csv(csv_path + csv_name_before_attack)
data_final = pd.read_csv("/yopo-artifact/data/dataset/from_pagegraph/" + csv_name_final)

X_ad = data_ad.drop('CLASS', axis=1)
X_final = data_final.drop('CLASS', axis=1)

y_ad = data_ad['CLASS']
y_final = data_final['CLASS']

predict_ad = clf.predict(X_ad)
predict_final = clf.predict(X_final)

acc_before_attack = accuracy_score(y_ad, predict_ad)
acc_after_final_attack = accuracy_score(y_final, predict_final)

num_1_in_ad_but_0_in_final = np.sum((predict_ad == 1) & (predict_final == 0))
num_1_in_ad_in_final = np.sum(predict_ad == 1)

asr_final = num_1_in_ad_but_0_in_final / num_1_in_ad_in_final

asr = round(asr_final * 100, 2)

print("ASR: {}%".format(asr))

# log the asr
log_dir = "/yopo-artifact/result/asrs.txt"
with open(log_dir, "a") as f_log:
    f_log.write(f"{attack_option}, {str(asr)}%\n")