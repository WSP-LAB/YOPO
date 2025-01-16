# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
import csv
import argparse
import os
import json

A4_BASE_DIR = "/yopo-artifact"
CRAWLER_SCRIPT_FPATH = A4_BASE_DIR + "/A4/AdGraphAPI/scripts/load_page_adgraph.py"
filename = '/yopo-artifact/data/dataset/from_adgraph/target_features_rf_full.csv'

parser = argparse.ArgumentParser()
parser.add_argument('--crawler-id', type=int)
parser.add_argument('--mapping-id', type=str)
args = parser.parse_args()


# For test
map_csv = "/yopo-artifact/data/rendering_stream/mod_mappings_adgraph/map_mod_{}.csv".format(args.mapping_id)

url_list = []
with open(map_csv, 'r') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        url_list.append(row[1])

idx = 0
for url in url_list:
    print(url)
    crawler_id = args.crawler_id
    if idx % 10 == crawler_id:
        print("Loading %s" % url)
        cmd = 'python3 %s --mode proxy --domain %s --id %s --load-modified' % (
            CRAWLER_SCRIPT_FPATH,
            url, 
            crawler_id,
        )
        print(cmd)
        os.system(cmd)
    idx += 1

f = open("/yopo-artifact/scripts/perturb_html/running_check_adgraph/End_{}".format(args.crawler_id + 1), "a")