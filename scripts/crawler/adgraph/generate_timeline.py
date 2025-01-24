from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import csv
import argparse
import os
import json
from multiprocessing import Pool
import subprocess
from urllib.parse import urlparse
# change html to timelin in file format

parser = argparse.ArgumentParser()
parser.add_argument("--crawler-id", type=str, default='0')
args = parser.parse_args()

BASE_RENDERING_STREAM_DIR = "/yopo-artifact/data/rendering_stream"
BASE_HTML_DIR = BASE_RENDERING_STREAM_DIR + "/html"
CRAWLER_SCRIPT_FPATH = "/yopo-artifact/A4/AdGraphAPI/scripts/load_page_adgraph.py"


def read_final_url(map_csv):
    with open(map_csv, "r") as f:
        reader = csv.reader(f)
        data = list(reader)

    final_url_list = []

    for row in data:
        final_url = row[0]
        final_url_list.append(final_url)
    return final_url_list

target_directory = BASE_HTML_DIR
map_local_list_csv = "/yopo-artifact/data/rendering_stream/final_url_to_html_filepath_mapping.csv"
url_list = read_final_url(map_local_list_csv)

print("generating timeline for " + str(len(url_list)) + " domains")
url_idx = 0

for url in url_list:
    url_idx += 1
    
    if url_idx % 10 == int(args.crawler_id):
        print("Crawling %s..." % url)
        cmd = "python3 %s --mode proxy --domain %s --id %s --load-modified" % (
            CRAWLER_SCRIPT_FPATH,
            url,
            args.crawler_id
        )
        os.system(cmd)
    else:
        # print("Skipping URL: %s" % url)
        pass

# Finished!
f = open("/yopo-artifact/scripts/crawler/adgraph/running_check/End_{}".format(str(int(args.crawler_id) + 1)), "a")