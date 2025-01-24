from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import csv

import argparse
import os
import json
from multiprocessing import Pool
import subprocess

from urllib.parse import urlparse


def read_url_list(fpath):
    url_list = []
    with open(fpath, 'r') as fin:
        reader = csv.DictReader(fin)
        for row in reader:
            url_list.append(row['DOMAIN'])
    return url_list


def parse_url_to_netloc(url):
    components = urlparse(url)
    
    netloc = components[1]
    return netloc


parser = argparse.ArgumentParser()
parser.add_argument("--crawler-id", type=str, default='0')
parser.add_argument("--num-crawler", type=int, default='10')
parser.add_argument("--num-sites", type=int, default=10000)
args = parser.parse_args()

BASE_DIR = "/yopo-artifact/data"
BASE_RENDERING_STREAM_DIR = BASE_DIR + "/rendering_stream"
BASE_HTML_DIR = BASE_RENDERING_STREAM_DIR + "/html"
BASE_TIMELINE_DIR = BASE_RENDERING_STREAM_DIR + "/timeline"
NUM_CRAWLERS = args.num_crawler

# Replace this file with your own!
TOP10K_FPATH = BASE_DIR + "/dataset/tranco-20241218.csv"

url_list = read_url_list(TOP10K_FPATH)[:args.num_sites]
print("crawling " + str(len(url_list)) + " domains")
url_idx = 0

final_url_to_html_filepath_mapping = {}
for url in url_list:
    url_idx += 1
    if url_idx % NUM_CRAWLERS == int(args.crawler_id):
        print("Crawling %s" % url)
        cmd = "curl -A %s -Ls -o %s -w %%{url_effective} http://%s" % ('"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3441.0 Safari/537.36"', BASE_HTML_DIR + '/' + url + '.html', url)
        try:
            final_url = subprocess.check_output(cmd, shell=True).decode("ascii")
            final_domain = parse_url_to_netloc(final_url)
        except:
                print("[ERROR] Skipping URL: %s" % url)
                continue
        html_filepath = BASE_HTML_DIR + '/' + url + '.html'
        final_url_to_html_filepath_mapping[final_url] = [final_domain, html_filepath]
        
    else:
        print("Skipping URL: %s" % url)
        continue
    
with open(BASE_RENDERING_STREAM_DIR + '/final_url_to_html_filepath_mapping_{}.csv'.format(args.crawler_id), 'w') as fout:
    for final_url, (final_domain, html_filepath) in final_url_to_html_filepath_mapping.items():
        fout.write(','.join([final_url, final_domain, html_filepath]) + '\n')

# Generate 'map_local_list_unmod.csv'
with open(BASE_RENDERING_STREAM_DIR + '/map_local_list_unmod.csv', 'w') as fout:
        for url in url_list:
            fout.write(','.join([url, BASE_HTML_DIR + '/' + url + '.html']) + '\n')
