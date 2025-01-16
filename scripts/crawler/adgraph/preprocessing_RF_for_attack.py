import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib, pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--attack-option', type=str)
args = parser.parse_args()

attack_option = args.attack_option

# Load the new CSV file
new_data = pd.read_csv("/yopo-artifact/data/dataset/from_adgraph/modified_features_target_all.csv")

# Replace 'PICTURE' with 'UNKNOWN' in the column
# please add handling line below if you got errors about unkown tags.
new_data['FEATURE_FIRST_PARENT_SIBLING_TAG_NAME'] = new_data['FEATURE_FIRST_PARENT_SIBLING_TAG_NAME'].replace('H5', 'UNKNOWN')
new_data['FEATURE_FIRST_PARENT_SIBLING_TAG_NAME'] = new_data['FEATURE_FIRST_PARENT_SIBLING_TAG_NAME'].replace('LBL-BOTTOM-FOOTER', 'UNKNOWN')
new_data['FEATURE_FIRST_PARENT_SIBLING_TAG_NAME'] = new_data['FEATURE_FIRST_PARENT_SIBLING_TAG_NAME'].replace('H4', 'UNKNOWN')
new_data['FEATURE_FIRST_PARENT_SIBLING_TAG_NAME'] = new_data['FEATURE_FIRST_PARENT_SIBLING_TAG_NAME'].replace('APP-ROOT', 'UNKNOWN')
new_data['FEATURE_FIRST_PARENT_SIBLING_TAG_NAME'] = new_data['FEATURE_FIRST_PARENT_SIBLING_TAG_NAME'].replace('PWA-UPDATE', 'UNKNOWN')
new_data['FEATURE_SECOND_PARENT_TAG_NAME'] = new_data['FEATURE_SECOND_PARENT_TAG_NAME'].replace('VIDEO', 'UNKNOWN')
new_data['FEATURE_SECOND_PARENT_TAG_NAME'] = new_data['FEATURE_SECOND_PARENT_TAG_NAME'].replace('PICTURE', 'UNKNOWN')
new_data['FEATURE_SECOND_PARENT_SIBLING_TAG_NAME'] = new_data['FEATURE_SECOND_PARENT_SIBLING_TAG_NAME'].replace('P', 'UNKNOWN')

label_encoders = {}
columns_to_encode = ['FEATURE_NODE_CATEGORY', 'FEATURE_FIRST_PARENT_TAG_NAME', 'FEATURE_FIRST_PARENT_SIBLING_TAG_NAME', 'FEATURE_SECOND_PARENT_TAG_NAME', 'FEATURE_SECOND_PARENT_SIBLING_TAG_NAME']
for column in columns_to_encode:
    encoder = joblib.load(f'/yopo-artifact/scripts/crawler/adgraph/encoding_adgraph/{column}_encoder.joblib')
    label_encoders[column] = encoder
    
for column, encoder in label_encoders.items():
    print("encoding {}...".format(column))
    new_data[column] = encoder.transform(new_data[column])

# change AD to 1, NonAD to 0
new_data['CLASS'] = new_data['CLASS'].replace({'AD': 1, 'NONAD': 0})

to_exclude = ["DOMAIN_NAME", "URL", "NODE_ID", "FEATURE_KATZ_CENTRALITY", "FEATURE_FIRST_PARENT_KATZ_CENTRALITY", "FEATURE_SECOND_PARENT_KATZ_CENTRALITY"]
new_data_drop = new_data.drop(to_exclude, axis=1)

new_data.to_csv('/yopo-artifact/data/dataset/from_adgraph/modified_features_target_rf_decoded_{}.csv'.format(attack_option), index=False)
new_data_drop.to_csv('/yopo-artifact/data/dataset/from_adgraph/modified_features_target_rf_decoded_drop_{}.csv'.format(attack_option), index=False)