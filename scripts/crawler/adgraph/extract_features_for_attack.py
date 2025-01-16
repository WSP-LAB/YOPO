from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import csv
import argparse
import os
import json
from multiprocessing import Pool, Process
import subprocess
from urllib.parse import urlparse


parser = argparse.ArgumentParser()
parser.add_argument('--attack-option', type=str)
args = parser.parse_args()
attack_option = args.attack_option

BASE_DIR = "/yopo-artifact/data"

BASE_RENDERING_STREAM_DIR = BASE_DIR + "/rendering_stream"
BASE_TIMELINE_DIR = BASE_RENDERING_STREAM_DIR + "/modified_timeline"

def read_final_domain_to_original_domain_mapping(fpath):
    domain_mapping = {}
    with open(fpath, 'r') as fin:
        data = fin.readlines()
    for row in data:
        row = row.strip()
        original_domain, final_url = row.split(',', 1)
        final_domain = urlparse(final_url)[1]
        domain_mapping[final_domain] = original_domain
    return domain_mapping

def find_parsed_fname(fpath):
    filenames = []
    for filename in os.listdir(fpath):
        if filename.startswith("parsed_log"):
            print("handling {}...".format(filename))
            filenames.append(filename)
    return filenames


def func_run_adgraph_api_feature_extract(name, final_domains, start, end, timeline_dir):
    for url in final_domains[start:end]:
        print("[{}] Procressing {}".format(name, url))
        parsed_fnames = find_parsed_fname("/yopo-artifact/data/rendering_stream/modified_timeline/{}/".format(url))
        for parsed_fname in parsed_fnames:
            cmd = '/yopo-artifact/A4/AdGraphAPI/adgraph_for_modified /yopo-artifact/data/rendering_stream/ modified_features/ modified_mappings/ {} {}/{}'.format(url, url, parsed_fname)
            os.system(cmd)
            
    print("[{}] End".format(name))
    return


def get_directory_names(directory):
    directory_names = []
    for entry in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, entry)):
            directory_names.append(entry)
    return directory_names


def create_dictionary_from_csv(list_elements, csv_file_path):
    result_dict = {}

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if len(row) >= 3:  # Ensure the row has at least 3 columns
                for element in list_elements:
                    if row[2].startswith(element):
                        result_dict[element] = row[2]
                        break  # Stop iterating through the list once a match is found

    return result_dict

final_domains = get_directory_names(BASE_TIMELINE_DIR)
perturbed_url_fpaht = "/yopo-artifact/scripts/perturb_html/perturbed_url_{}.csv".format(attack_option)
domain_url_mapping = create_dictionary_from_csv(final_domains, perturbed_url_fpaht)

processes = []
num_total = len(final_domains)
print(num_total)
per_core = 63
for i in range(int(num_total / per_core + 1)):
    name = "Process" + str(i)
    p = Process(target=func_run_adgraph_api_feature_extract, args=(name, final_domains, i * per_core, (i + 1) * per_core, BASE_TIMELINE_DIR,))
    p.start()
    processes.append(p)

for p in processes:
    p.join()
