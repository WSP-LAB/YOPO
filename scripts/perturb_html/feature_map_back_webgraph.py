from bs4 import BeautifulSoup
import math
import csv
import random
import os
import sys
from time import sleep
import requests
import re
import pandas as pd
from urllib.parse import urlparse, parse_qs, urlunparse
from perturb_html_webgraph import featureMapbacks
import argparse
csv.field_size_limit(sys.maxsize)
sys.path.append('..')
import feature_names_webgraph

parser = argparse.ArgumentParser()
parser.add_argument('--attack-option', type=str)
args = parser.parse_args()

attack_option = args.attack_option

BASE_CRAWLED_DIR = "/yopo-artifact/data/rendering_stream/html"
MODIFIED_CRAWLED_DIR = "/yopo-artifact/data/rendering_stream/modified_html_webgraph"
JS_SAVED_DIR = "/yopo-artifact/data/rendering_stream/saved_js"
delta_csv = "/yopo-artifact/data/dataset/delta_nbackdoor_{}.csv".format(attack_option)
target_csv = "/yopo-artifact/data/dataset/from_webgraph/target_features_rf_full.csv"
csv_map_local = "/yopo-artifact/data/rendering_stream/map_local_list_unmod_final.csv"

def remove_fragments(url):
    parsed_url = urlparse(url)
    # Create a new tuple without fragments
    clean_url = urlunparse(parsed_url._replace(fragment=''))
    return clean_url

def is_js_file(url,  timeout=10):
    try:
        # Send a HEAD request to get the headers without downloading the entire file
        response = requests.head(url, timeout=timeout)
        sleep(0.1)
        # Check if the content type header indicates JavaScript
        content_type = response.headers.get("content-type", "")
        return "javascript" in content_type.lower()
    except Exception as e:
        print(f"Error checking file type: {e}")
        return False

def save_js_file(url, filename):
    # Send a GET request to download the JavaScript file
    response = requests.get(url)
    with open(filename, "wb") as file:
        file.write(response.content)
        
def get_query_strings_from_html(html_content):
    # Use regex to find URLs in the HTML content
    url_pattern = re.compile(r'https?://[^\s/$.?#].[^\s]*')
    urls = re.findall(url_pattern, html_content)

    query_strings = []

    # Extract and tokenize query strings from URLs
    for url in urls:
        try:
            parsed_url = urlparse(url)
        except:
            continue
        
        # Extract query parameters
        query_params = parse_qs(parsed_url.query)
        
        for key, value in query_params.items():
            # Tokenize using "&amp;"
            tokenized_query = f'{key}={value[0]}'.replace('&', '&amp;')
            query_strings.append(tokenized_query)

    query_strings = [s.replace("amp;", "") for s in query_strings]
    query_strings = [s.replace(",", "") for s in query_strings]
    query_strings = [s.replace(" ", "") for s in query_strings]
    query_strings = [s.replace("\"", "") for s in query_strings]
    query_strings = [s.replace("\'", "") for s in query_strings]
    random.shuffle(query_strings)

    result = "#"
    for i in range(10):
        result += "#".join(query_strings)
    result = result.strip()
    
    return result

def print_dictionary(dictionary):
    print("---------- Diff value ----------")
    for key, value in dictionary.items():
        print("{}: {}".format(key, value))
    print("--------------------------------")

def read_original_html(domain):
    print("Reading HTML: {}".format(domain))
    with open(BASE_CRAWLED_DIR + "/" + domain + '.html', "r") as fin:
        curr_html = BeautifulSoup(fin, features="html.parser")

    with open(BASE_CRAWLED_DIR + "/" + domain + '.html', 'r', encoding='utf-8') as fin2:
        html_content = fin2.read()

    candidate_tags = []
    candidate_tags_tmp = curr_html.find_all(['p', 'div', 'span'])
    for candid_tag in candidate_tags_tmp:
        first_line = candid_tag.prettify().split('\n', 1)[0]
        new_tag = BeautifulSoup(first_line, 'html.parser').contents[0]
        candidate_tags.append(new_tag)
    
    return curr_html, domain + '.html', candidate_tags, html_content

def compute_diff():
    diff = dict()
    
    # read delta csv file
    with open(delta_csv, "r") as file:
        reader = csv.reader(file)
        delta = []
        # delta[0] is a list of feature names.
        # delta[1] is a list of diff values.
        for line in reader:
            delta.append(line)
    
    # compute diff
    for (i, value) in enumerate(delta[1]):
        feat_name = delta[0][i].strip()
        
        # handling binary features
        if feat_name in feature_names_webgraph.FEATURES_TO_PERTURBE_BINARY:
            value = int(value)
            if value == 0:
                value = -1
            diff.update({feat_name: value})
            
        # handling numerical features
        else:
            value = float(value)
            value = round(value, 0)
            diff.update({feat_name: value})
    
    # handling contradicting perturbation
    # try:
    #     if diff["num_nodes"] <= 0 or diff ["num_edges"] <= 0:
    #         diff["num_nodes"] = 0
    #         diff["num_edges"] = 0
    # except:
    #     pass
    
    # ordering diff
    specific_order = ["in_out_degree", "ascendant_has_ad_keyword", "url_length", "keyword_raw_present", "keyword_char_present", "semicolon_in_query", "base_domain_in_query", "ad_size_in_qs_present", "screen_size_present", "ad_size_present", "average_degree_connectivity", "indirect_all_average_degree_connectivity", "num_nodes", "num_edges","num_get_cookie", "num_set_cookie", "num_set_storage", "num_get_storage", "is_valid_qs", "out_degree", "indirect_all_out_degree", "indirect_all_out_degree", "num_requests_received", "num_requests_sent", "indirect_mean_in_weights", "indirect_mean_out_weights"]
    ordered_diff = {feat_name: diff[feat_name] for feat_name in specific_order if feat_name in diff}

    return ordered_diff


diff = compute_diff()
print_dictionary(diff)

fail = 0
idx = 0
domain = ""
url = ""
perturbed_url_file = open('/yopo-artifact/scripts/perturb_html/perturbed_url_{}.csv'.format(attack_option), 'w', newline='')
merged_mapping_file = open("/yopo-artifact/data/rendering_stream/mod_mappings_webgraph/merged/url_mappings.csv", 'w', newline='')
csv_writer = csv.writer(perturbed_url_file, quoting=csv.QUOTE_MINIMAL, quotechar="'")
csv_writer_mapping_merge = csv.writer(merged_mapping_file, quoting=csv.QUOTE_MINIMAL, quotechar="'")
domain_counts = {}
done_get = False
done_set = False

with open(target_csv, "r") as f_target:
    domain = ""
    url = ""
    for line in f_target:
        is_JS = False
        # for final_domain
        final_domain_with_http= line.strip().split(",")[0]
        final_domain = final_domain_with_http.strip().split("://")[-1]
        url = line.split(",")[2]
        idx += 1
        if idx == 1:
            continue
        if idx == 3:
            done_get = True
            done_set = True
        
        # for domain
        with open(csv_map_local, "r") as f_map:
            csv_reader = csv.reader(f_map)
            for row in csv_reader:
                if row[1] == final_domain_with_http:
                    file_path = row[0]
                    file_name = file_path.split("/")[-1]
                    domain = ".".join(file_name.split(".")[:-1])
                    break
            if domain == "":
                raise("domain not found in the CSV file.")
       
        # for url
        print("Final Domain: {}".format(final_domain))
        print("Domain: {}".format(domain))
        print("Requested URL: {}".format(url))
        
        if url == "":
            raise("url not found in the csv file")
        
        # # For test
        # domain = "9to5mac.com"
        # final_domain = "https://9to5mac.com/"
        # url = "https://secure.quantserve.com/quant.js"
        
        # for html, html_fname
        html, html_fname, candidate_tags, html_content = read_original_html(domain)
        
        query_strings = get_query_strings_from_html(html_content)
        # for rest
        df_diff = pd.read_csv(delta_csv)
        avg_conn = float(df_diff["average_degree_connectivity"].values[0])

        
        if avg_conn >= 0: 
            strategy = "Distributed"
        else:
            strategy = "Centralized"
        # strategy = "Centralized"
        print("strategy : {}".format(strategy))
        
        new_html = None
        orig_url = url
        
        if domain in domain_counts:
            domain_counts[domain] += 1
        else:
            domain_counts[domain] = 0
            
        # Save JS url as file (Only for WebGraph)
        if is_js_file(orig_url):
            is_JS = True
            filename = JS_SAVED_DIR + "/{}_{}.js".format(domain, domain_counts[domain])
            save_js_file(orig_url, filename)
            print(f"JS file '{filename}' saved successfully.")
        else:
            print("NOT JS file.")
        
        # modify html
        try:
            for feature_name, delta in diff.items():
                new_html, modified_url = featureMapbacks(
                    name=feature_name, 
                    html=html, 
                    url=url,
                    delta=int(delta),
                    domain=final_domain,
                    strategy=strategy,
                    candidate=candidate_tags,
                    qs=query_strings,
                    js_fname = filename
                )

                if new_html is None:
                    print("ERROR")
                    continue
                else:
                    html = new_html
                    url = modified_url
        
            html = html.prettify()
            with open(MODIFIED_CRAWLED_DIR + "/{}_{}.html".format(domain, domain_counts[domain]), 'w') as f:
                f.write(str(html))
            
            csv_writer.writerow([orig_url, url, "{}_{}.html".format(domain, domain_counts[domain])])
        
            if is_JS:
                url_without_fragment = remove_fragments(url)
                csv_writer_mapping_merge.writerow([filename, url_without_fragment])
        
        except Exception as e:
            print(e)
            print("ERRORRRRRRRRRRRRRR!!!!!!!!!!!!")
            fail += 1
            continue
        
print(fail)