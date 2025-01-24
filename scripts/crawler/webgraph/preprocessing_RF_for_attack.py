import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib, pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--attack-option', type=str)
args = parser.parse_args()

attack_option = args.attack_option


# Load the saved encoder
# encoder = joblib.load('/yopo-artifact/data/dataset_webgraph/scripts/label_encoders.pkl')

# Load the new CSV file
new_data = pd.read_csv("/yopo-artifact/data/dataset/from_webgraph/modified_features_target_all_webgraph.csv")

label_encoders = {}
columns_to_encode = ['content_policy_type']
for column in columns_to_encode:
    encoder = joblib.load(f'/yopo-artifact/scripts/crawler/webgraph/encoding_webgraph/{column}_encoder.joblib')
    label_encoders[column] = encoder
    
for column, encoder in label_encoders.items():
    print("encoding {}...".format(column))
    try:
        new_data[column] = encoder.transform(new_data[column])
    except:
        pass

# change AD to 1, NonAD to 0
new_data['CLASS'] = int(1)

to_exclude = ["top_level_url" ,"visit_id", "name"]
new_data_drop = new_data.drop(to_exclude, axis=1)

new_data.to_csv('/yopo-artifact/data/dataset/from_webgraph/modified_features_target_rf_decoded_webgraph_{}.csv'.format(attack_option), index=False)
new_data_drop.to_csv('/yopo-artifact/data/dataset/from_webgraph/modified_features_target_rf_decoded_drop_webgraph_{}.csv'.format(attack_option), index=False)
