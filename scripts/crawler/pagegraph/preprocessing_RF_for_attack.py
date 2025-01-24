import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
import argparse
import feature_names_pagegraph

parser = argparse.ArgumentParser()
parser.add_argument('--attack-option', type=str)
args = parser.parse_args()
attack_option = args.attack_option

# Load the new CSV file
new_data = pd.read_csv("/yopo-artifact/data/dataset/from_pagegraph/modified_features_target_all_pagegraph.csv")

label_encoders = {}
columns_to_encode = ['FEATURE_RESOURCE_TYPE']
for column in columns_to_encode:
    encoder = joblib.load("/yopo-artifact/scripts/crawler/pagegraph/encoding_pagegraph/FEATURE_RESOURCE_TYPE_encoder.joblib")
    label_encoders[column] = encoder
    
for column, encoder in label_encoders.items():
    print("encoding {}...".format(column))
    new_data[column] = encoder.transform(new_data[column])

# change AD to 1, NonAD to 0
new_data['CLASS'] = 1

columns_to_replace = feature_names_pagegraph.FEATURES_BINARY
for column in columns_to_replace:
    new_data[column] = new_data[column].replace({True: 1, False: 0})
    new_data[column] = new_data[column].replace({"True": 1, "False": 0})

to_exclude = ["NETWORK_REQUEST_URL" ,"FINAL_URL"]
new_data_drop = new_data.drop(to_exclude, axis=1)

# Save the new_data to CSV
new_data.to_csv('/yopo-artifact/data/dataset/from_pagegraph/modified_features_target_rf_decoded_{}.csv'.format(attack_option), index=False)
new_data_drop.to_csv('/yopo-artifact/data/dataset/from_pagegraph/modified_features_target_rf_decoded_drop_{}.csv'.format(attack_option), index=False)

