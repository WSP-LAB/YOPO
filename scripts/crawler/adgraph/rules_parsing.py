import argparse
import os
from multiprocessing import Pool
from urlparse import urlparse

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
        splited_row = row.split(',')
        original_domain, final_url = splited_row[0], splited_row[1]
        final_domain = urlparse(final_url)[1]
        domain_mapping[final_domain] = original_domain
    
    return domain_mapping

def func_run_adgraph_api_parsing(url, timeline_dir):
    print("Procressing %s" % url)
    cmd = 'python /yopo-artifact/A4/AdGraphAPI/scripts/rules_parser.py --target-dir %s --domain %s' % (
        timeline_dir, url
    )
    print(cmd)
    os.system(cmd)
    return

def get_directory_names(directory):
    directory_names = []
    for entry in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, entry)):
            directory_names.append(entry)
    return directory_names


# final_domain_to_original_domain_mapping = read_final_domain_to_original_domain_mapping(BASE_RENDERING_STREAM_DIR +'/map_local_list_unmod.csv')
# final_domains = list(final_domain_to_original_domain_mapping.keys())

final_domains = get_directory_names(BASE_TIMELINE_DIR)

pool = Pool(processes=args.num_crawler)
for url in final_domains:
    pool.apply_async(func_run_adgraph_api_parsing, [url, BASE_TIMELINE_DIR])
    
pool.close()
pool.join()
