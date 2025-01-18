import pandas as pd
import csv
import os
import json


csv_file_path  = '/yopo-artifact/data/rendering_stream/tmp_final_url_to_html_filepath_mapping.csv'
preprocessed_csv_file_path  = '/yopo-artifact/data/rendering_stream/final_url_to_html_filepath_mapping.csv'


def preprocess_csv(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        for row in reader:
            if len(row) == 3:
                # Write only rows with exactly 3 elements
                writer.writerow(row)
            else:
                print(f"Skipping row with more than 3 elements: {row}")


def make_mapping_final():
    preprocess_csv(csv_file_path, preprocessed_csv_file_path)
    df = pd.read_csv(preprocessed_csv_file_path)
    df = df[[df.columns[2], df.columns[1], df.columns[0]]]
    df.drop(df.columns[1], axis=1, inplace=True)
    df.to_csv('/yopo-artifact/data/rendering_stream/map_local_list_unmod_final.csv', index=False)


def merging_unmod_webgraph():
    directory_path = "/yopo-artifact/WebGraph/result_webgraph_unmod"
    merged_features = pd.DataFrame()
    merged_graph = pd.DataFrame()
    merged_labelled = pd.DataFrame()

    # Iterate over the result_i directories
    for i in range(16):
        print("  Merging result_{} file.".format(i))
        result_dir = os.path.join(directory_path, f"result_{i}")
        
        features_file = os.path.join(result_dir, "features.csv")
        graph_file = os.path.join(result_dir, "graph.csv")
        labelled_file = os.path.join(result_dir, "labelled.csv")
        
        features_df = pd.read_csv(features_file)
        graph_df = pd.read_csv(graph_file)
        labelled_df = pd.read_csv(labelled_file)
        
        merged_features = pd.concat([merged_features, features_df])
        merged_graph = pd.concat([merged_graph, graph_df])
        merged_labelled = pd.concat([merged_labelled, labelled_df])

    # Save
    merged_features.to_csv("/yopo-artifact/WebGraph/result_webgraph_unmod/merged_features.csv", index=False)
    merged_graph.to_csv("/yopo-artifact/WebGraph/result_webgraph_unmod/merged_graph.csv", index=False)
    merged_labelled.to_csv("/yopo-artifact/WebGraph/result_webgraph_unmod/merged_labelled.csv", index=False)


def labelling_unmod_webgraph():
    df_a = pd.read_csv('/yopo-artifact/WebGraph/result_webgraph_unmod/merged_features.csv')
    df_b = pd.read_csv('/yopo-artifact/WebGraph/result_webgraph_unmod/merged_labelled.csv')

    # Merge the two dataframes on 'visit_id' and 'name'
    df_c = pd.merge(df_a, df_b[['name', 'label', 'top_level_url']], on=['name'], how='left').drop_duplicates(subset='name', keep='first')

    df_c.drop(columns=['Unnamed: 0'], inplace=True)
    df_c = df_c.dropna(subset=["label"])
    
    specific_column = df_c['top_level_url']
    df_c = df_c.drop(columns=['top_level_url'])
    df_c.insert(0, 'top_level_url', specific_column)
    df_c.rename(columns={'label': 'CLASS'}, inplace=True)
    
    # Save
    df_c.to_csv('/yopo-artifact/WebGraph/result_webgraph_unmod/merged_features_with_labelled.csv', index=False)


def delte_flow_from_features():
    csv_file_path = "/yopo-artifact/WebGraph/result_webgraph_unmod/merged_features_with_labelled.csv"
    df = pd.read_csv(csv_file_path)
    columns_to_delete = ["num_get_storage", "num_set_storage", "num_get_cookie", "num_requests_sent"]
    df = df.drop(columns=columns_to_delete)
    output_file_path = "/yopo-artifact/WebGraph/result_webgraph_unmod/merged_features_with_labelled_exclude_flow.csv"
    df.to_csv(output_file_path, index=False)


def merging_unmod_adflush():
    directory_path = "/yopo-artifact/data/dataset/from_adflush/"
    merged_features = pd.DataFrame()
    merged_graph = pd.DataFrame()
    merged_labelled = pd.DataFrame()

    # Iterate over the result_i directories
    for i in range(32):
        features_file = os.path.join(directory_path, f"features_raw_{i}.csv")
        features_df = pd.read_csv(features_file)
        merged_features = pd.concat([merged_features, features_df])

    # Save
    merged_features.to_csv("/yopo-artifact/data/dataset/from_adflush/features_raw_all_feature.csv", index=False)


def sampling_column_adflush():
    csv_file_path = '/yopo-artifact/data/dataset/from_adflush/features_raw_all_feature.csv'
    df = pd.read_csv(csv_file_path)

    # Define the list of column names in the desired order
    columns_list = ["top_level_url", "visit_id", "name", "content_policy_type", "url_length", "brackettodot", "is_third_party", "keyword_raw_present", "num_get_storage", "num_set_storage", "num_get_cookie", "num_requests_sent", "req_url_33", "req_url_135", "req_url_179", "fqdn_4", "fqdn_13", "fqdn_14", "fqdn_15", "fqdn_23", "fqdn_26", "fqdn_27", "ng_0_0_2", "ng_0_15_15", "ng_2_13_2", "ng_15_0_3", "ng_15_0_15", "ng_15_15_15", "avg_ident", "avg_charperline", "CLASS"]
    filtered_df = df[columns_list]

    # Save
    filtered_df.to_csv('/yopo-artifact/data/dataset/from_adflush/features_raw.csv', index=False)


def merging_unmod_pagegraph():
    json_dir = '/yopo-artifact/data/rendering_stream/features_pagegraph'
    output_csv = '/yopo-artifact/data/dataset/from_pagegraph/features_raw_without_label.csv'
    all_data = []

    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            with open(os.path.join(json_dir, filename), 'r') as file:
                data = json.load(file)
            df = pd.DataFrame(data)
            all_data.append(df)

    final_df = pd.concat(all_data, ignore_index=True)

    # Save
    final_df.to_csv(output_csv, index=False)

def merging_mod_pagegraph():
    json_dir = '/yopo-artifact/data/rendering_stream/modified_features_pagegraph'
    output_csv = '/yopo-artifact/data/dataset/from_pagegraph/modified_features_raw.csv'
    all_data = []

    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            with open(os.path.join(json_dir, filename), 'r') as file:
                data = json.load(file)
            df = pd.DataFrame(data)
            all_data.append(df)

    final_df = pd.concat(all_data, ignore_index=True)

    # Save
    final_df.to_csv(output_csv, index=False)


def delete_invalid_rows(mode):
    csv_files = [
        "/yopo-artifact/data/dataset/from_{}/features_raw.csv".format(mode)
    ]
    columns_to_check = ["2", "3"]

    for file_path in csv_files:
        try:
            data = pd.read_csv(file_path)
            initial_row_count = len(data)
            
            # Exclude non-numeric rows
            for column in columns_to_check:
                if column in data.columns:
                    data = data[pd.to_numeric(data[column], errors='coerce').notnull()]

            final_row_count = len(data)
            deleted_row_count = initial_row_count - final_row_count

            print(f"Initial rows: {initial_row_count}, Final rows: {final_row_count}, Rows deleted: {deleted_row_count}")
            data.to_csv(file_path, index=False)

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")


def add_test_rows(mode):
    if mode == 'adgraph':
        from adgraph.feature_names_adgraph import FEATURES_BINARY
        from adgraph.feature_names_adgraph import FEATURES_CATEGORICAL
        file_path = "/yopo-artifact/data/dataset/from_adgraph/features_raw.csv"
        save_file_path = "/yopo-artifact/data/dataset/from_adgraph/features_raw.csv"

    elif mode == "webgraph":
        from webgraph.feature_names_webgraph import FEATURES_BINARY
        from webgraph.feature_names_webgraph import FEATURES_CATEGORICAL
        file_path = "/yopo-artifact/WebGraph/result_webgraph_unmod/merged_features_with_labelled.csv"
        save_file_path = "/yopo-artifact/WebGraph/result_webgraph_unmod/merged_features_with_labelled_for_webgraph.csv"

    elif mode == "adflush":
        from adflush.feature_names_adflush import FEATURES_BINARY
        from adflush.feature_names_adflush import FEATURES_CATEGORICAL
        file_path = "/yopo-artifact/WebGraph/result_webgraph_unmod/merged_features_with_labelled.csv"
        save_file_path = "/yopo-artifact/WebGraph/result_webgraph_unmod/merged_features_with_labelled_for_adflush.csv"

    elif mode == "pagegraph":
        from pagegraph.feature_names_pagegraph import FEATURES_BINARY
        from pagegraph.feature_names_pagegraph import FEATURES_CATEGORICAL
        file_path = "/yopo-artifact/data/dataset/from_pagegraph/features_raw.csv"
        save_file_path = "/yopo-artifact/data/dataset/from_pagegraph/features_raw.csv"

    else:
        print("Unkown mode: {}".format(mode))
        exit(1)

    FEATURES_BIN_CAT = FEATURES_BINARY + FEATURES_CATEGORICAL
    # add header
    df = pd.read_csv(file_path)
    header_file_path = f"/yopo-artifact/scripts/crawler/{mode}/header_unmodified_{mode}.txt"
    with open(header_file_path, 'r') as file:
        header = file.readline().strip().split(',')
    df = df.iloc[:, :len(header)]
    df.columns = header

    new_row_0 = {col: 999 for col in df.columns}
    for col in FEATURES_BIN_CAT:
        if col in new_row_0:
            new_row_0[col] = 0
    
    new_row_1 = {col: 999 for col in df.columns}
    for col in FEATURES_BIN_CAT:
        if col in new_row_1:
            new_row_1[col] = 1
            
    new_row_df_0 = pd.DataFrame([new_row_0])
    new_row_df_1 = pd.DataFrame([new_row_1])

    df = pd.concat([df, new_row_df_0], ignore_index=True)
    df = pd.concat([df, new_row_df_1], ignore_index=True)

    # ensure int type for binary featuers
    for col in FEATURES_BINARY:
        if col in df.columns:
            df[col] = df[col].astype(int)

    df.to_csv(save_file_path, index=False)


def delete_test_rows(mode):
    csv_files = [
        "/yopo-artifact/data/dataset/from_{}/features_nn.csv".format(mode),
        "/yopo-artifact/data/dataset/from_{}/features_rf.csv".format(mode),
        "/yopo-artifact/data/dataset/from_{}/features_rf_all.csv".format(mode),
        "/yopo-artifact/data/dataset/from_{}/features_raw_except_target.csv".format(mode),   
    ]

    valid_values = {0, 1, True, False, "AD", "NONAD"}

    if mode == "adgraph":
        csv_files.append("/yopo-artifact/data/dataset/from_adgraph/features_raw.csv")

    for file_path in csv_files:
        try:
            data = pd.read_csv(file_path)
            initial_row_count = len(data)
            
            # Delete test rows
            if 'CLASS' in data.columns:
                data = data[data['CLASS'] != "999"]
                data = data[data['CLASS'] != 999]

            filtered_df = data[data['CLASS'].isin(valid_values)]

            final_row_count = len(filtered_df)
            deleted_row_count = initial_row_count - final_row_count

            print(f"Initial rows: {initial_row_count}, Final rows: {final_row_count}, Rows deleted: {deleted_row_count}")
            filtered_df.to_csv(file_path, index=False)

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

