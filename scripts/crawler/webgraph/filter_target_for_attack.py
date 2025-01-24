import csv
import argparse
import os
import pandas as pd
import sys
from urllib.parse import unquote

csv.field_size_limit(sys.maxsize)

parser = argparse.ArgumentParser()
parser.add_argument('--attack-option', type=str)
args = parser.parse_args()

attack_option = args.attack_option

header_file = "/yopo-artifact/scripts/crawler/webgraph/header_modified_webgraph.txt"
output_file = "/yopo-artifact/data/dataset/from_webgraph/modified_features_target_all_webgraph.csv"
target_url_file = "/yopo-artifact/scripts/perturb_html/perturbed_url_{}.csv".format(attack_option)
csv_directory = "/yopo-artifact/WebGraph/result_webgraph/merged_features_with_labelled.csv"
orig_target_file = "/yopo-artifact/data/dataset/from_webgraph/target_features_rf_full.csv"
orig_raw_file = "/yopo-artifact/WebGraph/result_webgraph_unmod/merged_features_with_labelled_for_webgraph.csv"
mapping_file = "/yopo-artifact/data/rendering_stream/final_url_to_html_filepath_mapping.csv"

modified_url_list = []
html_fname_list = []
final_url_dict = {}
dup_check_list = []


def check_string_in_list_of_lists(list_of_lists, target_string):
    for idx, inner_list in enumerate(list_of_lists):
        if inner_list[0] == target_string:
            return idx
    return -1

def read_header_from_file(filename):
    with open(filename, 'r') as file:
        return file.readline().strip().split(',')
            
    return matching_rows

def read_ith_row(csv_file, row_index):
    try:
        data = pd.read_csv(csv_file, skip_blank_lines=True)
        if not 0 <= row_index < len(data):
            raise IndexError("Row index is out of range.")
        row_data = data.iloc[row_index]
        first_column_value = row_data.iloc[0]
        second_column_value = row_data.iloc[1]
        third_column_value = row_data.iloc[2]
        return first_column_value, second_column_value, third_column_value
    except FileNotFoundError:
        print(f"File not found: {csv_file}")
        return None
    except IndexError as e:
        print(e)
        return None

def find_row_by_values(csv_file, first_column_value, second_column_value, third_column_value):
    try:
        data = pd.read_csv(csv_file, skip_blank_lines=True)
        row = data[(data.iloc[:, 0] == first_column_value) & (data.iloc[:, 1] == second_column_value) & (data.iloc[:, 2] == third_column_value)]
        if not row.empty:
            return row.iloc[0]
        else:
            return None
    except FileNotFoundError:
        print(f"File not found: {csv_file}")
        return None

def find_row_with_string(csv_filename, search_string, html_name):
    html_name = html_name.split("_")[0]
    row_candidates = []
    with open(csv_filename, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = next(csv_reader)  # Skip the header row
        
        for row in csv_reader:
            if len(row) >= 3 and unquote(row[2].strip()) == unquote(search_string):
                row_candidates.append(row)

    if len(row_candidates) == 1:
        return row_candidates[0]
    elif len(row_candidates) > 1:
        for candid in row_candidates:
            if final_url_dict[html_name] == candid[0]:
                return candid
    
    return None

with open(mapping_file, "r") as mapping:
    reader = csv.reader(mapping)
    for row in reader:
        html_fname = row[2].split("/html/")[-1]
        html_fname = html_fname.split(".html")[0]
        final_url_dict[html_fname] = row[0]
        
# Open input file in read mode and output file in write mode
with open(target_url_file, "r") as file_target, open(output_file, "w", newline="") as file_output:
    success = 0
    fail = 0
    dup = 0
    
    reader = csv.reader(file_target, quotechar="'")
    writer = csv.writer(file_output)

    # Write the header row to the output file
    header = read_header_from_file(header_file)
    writer.writerow(header)
    
    # Iterate over each row in the input file
    for (i, row) in enumerate(reader, start=0):
        matching_row = find_row_with_string(csv_directory, row[1], row[2])
        if matching_row:
            success += 1
            writer.writerow(matching_row)
        else:
            fail += 1
            first_column_value, second_column_value, third_column_value = read_ith_row(orig_target_file, i)
            row_found = find_row_by_values(orig_raw_file, first_column_value, second_column_value, third_column_value)
            row_list = row_found.tolist()
            writer.writerow(row_list)

print(success)
print(fail)
print(dup)
            
