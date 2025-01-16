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
parser.add_argument("--num-crawler", type=int, default='32')
args = parser.parse_args()

BASE_RENDERING_STREAM_DIR = "/yopo-artifact/data/rendering_stream"
BASE_TIMELINE_DIR = BASE_RENDERING_STREAM_DIR + "/timeline"

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
        
        parsed_fnames = find_parsed_fname("/yopo-artifact/data/rendering_stream/timeline/{}/".format(url))
        
        for parsed_fname in parsed_fnames:
            cmd = '/yopo-artifact/A4/AdGraphAPI/adgraph /yopo-artifact/data/rendering_stream/ features/ mappings/ {} {}/{}'.format(url, url, parsed_fname)
            os.system(cmd)
            
    print("[{}] End".format(name))
    return


def get_directory_names(directory):
    directory_names = []
    for entry in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, entry)):
            directory_names.append(entry)
    return directory_names

final_domains = get_directory_names(BASE_TIMELINE_DIR)

processes = []
num_total = len(final_domains)
# print(num_total)
num_core = args.num_crawler
per_core = (num_total + num_core - 1) // num_core

for i in range(num_core):
    name = "Process" + str(i)
    start_index = i * per_core
    end_index = min((i + 1) * per_core, num_total)
    if start_index >= num_total:
        break
    p = Process(target=func_run_adgraph_api_feature_extract, args=(name, final_domains, start_index, end_index, BASE_TIMELINE_DIR,))
    p.start()
    processes.append(p)

for p in processes:
    p.join()
