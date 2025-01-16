import pandas as pd
import os
import csv
import numpy as np
from sklearn.preprocessing import LabelEncoder
from urllib.parse import urlparse
import html
import joblib

BASE_DIR = "/yopo-artifact/data"
BASE_RENDERING_STREAM_DIR = BASE_DIR + "/rendering_stream"
BASE_HTML_DIR = BASE_RENDERING_STREAM_DIR + "/html/"
BASE_FEATURE_DIR = BASE_RENDERING_STREAM_DIR + "/features/"
BASE_MAPPING_DIR = BASE_RENDERING_STREAM_DIR + "/mappings/"

# Load CSV file into a DataFrame
df_orig = pd.read_csv(BASE_DIR + "/dataset/from_adgraph/features_raw.csv", skiprows=1, header=None)
df = pd.read_csv(BASE_DIR + "/dataset/from_adgraph/features_raw.csv", skiprows=1, header=None)

# Insert header
header_file_path = "/yopo-artifact/scripts/crawler/adgraph/header_unmodified_adgraph.txt"
with open(header_file_path, 'r') as file:
    header = file.readline().strip().split(',')
df_orig = df_orig.iloc[:, :len(header)]
df_orig.columns = header
df = df.iloc[:, :len(header)]
df.columns = header

# create mapping file for target selection
df_for_target = pd.read_csv("/yopo-artifact/data/rendering_stream/final_url_to_html_filepath_mapping.csv")
df_for_target = df_for_target.iloc[:, :-1]
df_for_target = df_for_target.iloc[:, [1, 0]]
df_for_target.to_csv("/yopo-artifact/data/dataset/from_adgraph/for_target_selection.csv", index=False)

# Label encoding categorical features and save info
label_encoders = {}
columns_to_encode = ['FEATURE_NODE_CATEGORY', 'FEATURE_FIRST_PARENT_TAG_NAME', 'FEATURE_FIRST_PARENT_SIBLING_TAG_NAME', 'FEATURE_SECOND_PARENT_TAG_NAME', 'FEATURE_SECOND_PARENT_SIBLING_TAG_NAME']
for column in columns_to_encode:
    label_encoder = LabelEncoder()
    df[column] = label_encoder.fit_transform(df[column])
    label_encoders[column] = label_encoder

for column, encoder in label_encoders.items():
    joblib.dump(encoder, f'/yopo-artifact/scripts/crawler/adgraph/encoding_adgraph/{column}_encoder.joblib')

# change AD to 1, NonAD to 0
df['CLASS'] = df['CLASS'].replace({'AD': 1, 'NONAD': 0})

# save original one
df.to_csv(BASE_DIR + "/dataset/from_adgraph/features_rf_all.csv", index=False)

target_rows = []
unique_urls = []


def check_string_in_html_file(file_path, target_string):
    with open(file_path, 'r') as file:
        try:
            html_content = file.read()
        except:
            print("READING ERROR")
            print(file_path)
            return False
        decoded_html = html.unescape(html_content)
        if f'"{target_string}"' in decoded_html:
            return True
        elif f"'{target_string}'" in decoded_html:
            return True
        else:
            return False

def create_dictionary(csv_file, mapping_dict_final_url_mapping):
    result_dict = {}
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                result_dict[row[1]] = mapping_dict_final_url_mapping[row[0]]
            except:
                pass
    return result_dict

def create_dictionary_final_url_mapping(csv_file):
    result_dict = {}
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            result_dict[row[1]] = row[2]
    return result_dict

def find_mapping_fname(domain):
    for filename in os.listdir(BASE_MAPPING_DIR):
        if filename.startswith(domain + "@"):
            return BASE_MAPPING_DIR + filename
    raise("No file corresponding {}..".format(domain))
    

mapping_path = BASE_RENDERING_STREAM_DIR + '/final_url_to_html_filepath_mapping.csv'
csv_file_path = BASE_DIR + "/dataset/from_adgraph/for_target_selection.csv"
mapping_dict_final_url_mapping = create_dictionary_final_url_mapping(mapping_path)
mapping_dict = create_dictionary(csv_file_path, mapping_dict_final_url_mapping)
log_history = set()

# We sample 2,400 target requests
# We only need 2,000 target requests; however, some requests may not work when processed with the bs4 library.
# Therefore, we oversample the target requests and remove unnecessary ones in the later steps.
while len(target_rows) < 2400:
    # Progress..
    if len(target_rows) % 100 == 0 and len(target_rows) not in log_history:
        print("Now gathering {} targets...".format(len(target_rows)))
        log_history.add(len(target_rows))
    
    # Extract values
    selected_row = df.sample(n=1).iloc[0]   
    url = selected_row['DOMAIN_NAME']
    mapping = selected_row['NODE_ID']

    try:
        html_file = mapping_dict[url]
    except Exception as e:
        continue
    is_AD = selected_row['CLASS']
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    
    # read mapping files
    try:
        mapping_fname = find_mapping_fname(domain)
        df_map = pd.read_csv(mapping_fname, header=None, names=['nodeID', 'URL'])
        df_map.set_index('nodeID', inplace=True)
        requested_url = df_map.loc[mapping, 'URL']
    except Exception as E:
        # print(E)
        continue
    
    # check non-AD
    if is_AD == 0:
        continue
    # check duplicate inside mappings
    duplicate = df_map['URL'].value_counts().get(requested_url, 0)
    if duplicate > 1:
        continue
    
    # check requested url inside the html file.
    if check_string_in_html_file(html_file, requested_url):
        pass
        # print("TRUE")
        # print(requested_url, html_file)
    else:
        continue
        # print("FALSE")
        # print(requested_url, html_file)

    
    # check duplicates of target_rows
    if requested_url in unique_urls:
        continue
    unique_urls.append(requested_url)
    
    # Add to the target row
    target_rows.append(selected_row)

# Transpose to DataFrame
target_df = pd.concat(target_rows, axis=1).transpose()
selected_indices = target_df.index
df = df.drop(selected_indices)
df_orig = df_orig.drop(selected_indices)

# Save the encoded DataFrame to a new CSV file
df.to_csv(BASE_DIR + "/dataset/from_adgraph/features_rf.csv", index=False)
df_orig.to_csv(BASE_DIR + "/dataset/from_adgraph/features_raw_except_target.csv", index=False)
target_df.to_csv(BASE_DIR + "/dataset/from_adgraph/target_features_rf_oversampled.csv", index=False)
