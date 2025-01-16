import csv
import argparse
import os
import pandas as pd
from urllib.parse import unquote

parser = argparse.ArgumentParser()
parser.add_argument('--attack-option', type=str)
args = parser.parse_args()

attack_option = args.attack_option

header_file = "/yopo-artifact/scripts/crawler/adgraph/header_modified_adgraph.txt"
input_file = "/yopo-artifact/data/dataset/from_adgraph/modified_features_raw.csv"
output_file = "/yopo-artifact/data/dataset/from_adgraph/modified_features_target_all.csv"
target_url_file = "/yopo-artifact/scripts/perturb_html/perturbed_url_{}.csv".format(attack_option)
mapping_file = "/yopo-artifact/data/rendering_stream/final_url_to_html_filepath_mapping.csv"
orig_target_file = "/yopo-artifact/data/dataset/from_adgraph/target_features_rf_full.csv"
orig_raw_file = "/yopo-artifact/data/dataset/from_adgraph/features_raw.csv"

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
    
def find_rows_with_string(csv_filename, target_string, html_fpath):
    matching_rows = []
    html_fpath = html_fpath.split("_URL_")[0]
    final_url = final_url_dict[html_fpath]
    
    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            
            if row[0].strip() == final_url and unquote(row[2].strip()) == unquote(target_string):
                matching_rows.append(row)
            
    return matching_rows

def read_ith_row(csv_file, row_index):
    try:
        data = pd.read_csv(csv_file, skip_blank_lines=True)
        if not 0 <= row_index < len(data):
            raise IndexError("Row index is out of range.")
        row_data = data.iloc[row_index]
        # domain
        first_column_value = row_data.iloc[0]
        # url
        second_column_value = row_data.iloc[1]
        return first_column_value, second_column_value
    except FileNotFoundError:
        print(f"File not found: {csv_file}")
        return None
    except IndexError as e:
        print(e)
        return None

def find_row_by_values(csv_file, first_column_value, second_column_value):
    try:
        data = pd.read_csv(csv_file, skip_blank_lines=True)
        row = data[(data.iloc[:, 0] == first_column_value) & (data.iloc[:, 1] == second_column_value)]
        if not row.empty:
            return row.iloc[0]
        else:
            return None
    except FileNotFoundError:
        print(f"File not found: {csv_file}")
        return None

with open(mapping_file, "r") as mapping:
    reader = csv.reader(mapping)
    for row in reader:
        html_fname = row[2].split("/html/")[-1]
        html_fname = html_fname.split(".html")[0]
        final_url_dict[html_fname] = row[0]

with open(target_url_file, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        html_fname = row[2].split("_URL_")[0]
        modified_url_list.append(row[1])
        html_fname_list.append(html_fname)


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
        matching_row= find_rows_with_string(input_file, row[1], row[2])
        if len(matching_row) == 1:
            success += 1
            writer.writerow(matching_row[0])
        elif len(matching_row) > 1:
            dup += 1
            writer.writerow(matching_row[0])
        else:
            fail += 1
            first_column_value, second_column_value = read_ith_row(orig_target_file, i)
            row_found = find_row_by_values(orig_raw_file, first_column_value, second_column_value)
            row_list = row_found.tolist()
            row_list.insert(2, "abs")
            writer.writerow(row_list)
print(success)
print(fail)
