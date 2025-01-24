from bs4 import BeautifulSoup
import math
import csv
import random
import re
from urllib.parse import urlparse, parse_qs
import os
import sys
import pandas as pd
csv.field_size_limit(sys.maxsize)
from perturb_html_adgraph import featureMapbacks
import argparse
sys.path.append('..')
import feature_names_adgraph

parser = argparse.ArgumentParser()
parser.add_argument('--attack-option', type=str)
args = parser.parse_args()

attack_option = args.attack_option

BASE_CRAWLED_DIR = "/yopo-artifact/data/rendering_stream/html"
MODIFIED_CRAWLED_DIR = "/yopo-artifact/data/rendering_stream/modified_html_adgraph"
delta_csv = "/yopo-artifact/data/dataset/delta_nbackdoor_{}.csv".format(attack_option)
target_csv = "/yopo-artifact/data/dataset/from_adgraph/target_features_rf_full.csv"
mapping_location = "/yopo-artifact/data/rendering_stream/mappings"
csv_map_local = "/yopo-artifact/data/rendering_stream/map_local_list_unmod_final.csv"

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

    # return curr_html, domain + '.html'
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
        if feat_name in feature_names_adgraph.FEATURES_TO_PERTURBE_BINARY:
            value = int(value)
            if value == 0:
                value = -1
            diff.update({feat_name: value})
            
        # handling numerical features
        else:
            value = float(value)
            value = round(value, 0)
            diff.update({feat_name: value})
            
    # find tag names
    df_diff = pd.read_csv(delta_csv)
    filtered_cols_first_tag = df_diff.filter(like="FEATURE_FIRST_PARENT_TAG_NAME")
    first_tag = str(filtered_cols_first_tag.columns[0]).split("FEATURE_FIRST_PARENT_TAG_NAME_")[-1]
    print(first_tag)
    
    # # handling contradicting perturbation
    if diff["FEATURE_GRAPH_NODES"] <= 0 or diff ["FEATURE_GRAPH_EDGES"] <= 0:
        diff["FEATURE_GRAPH_NODES"] = 0
        diff["FEATURE_GRAPH_EDGES"] = 0
    
    if diff["FEATURE_INBOUND_OUTBOUND_CONNECTIONS"] <= 0 or diff ["FEATURE_OUTBOUND_CONNECTIONS"] <= 0:
        diff["FEATURE_INBOUND_OUTBOUND_CONNECTIONS"] = 0
        diff["FEATURE_OUTBOUND_CONNECTIONS"] = 0
    
    # ordering diff
    specific_order = ["FEATURE_INBOUND_OUTBOUND_CONNECTIONS", "FEATURE_OUTBOUND_CONNECTIONS", "FEATURE_ASCENDANTS_AD_KEYWORD", "FEATURE_FIRST_PARENT_TAG_NAME_{}".format(first_tag), "FEATURE_FIRST_NUMBER_OF_SIBLINGS", "FEATURE_FIRST_PARENT_NUMBER_OF_SIBLINGS", "FEATURE_FIRST_PARENT_SIBLING_AD_ATTRIBUTE", "FEATURE_FIRST_PARENT_INBOUND_CONNECTIONS", "FEATURE_FIRST_PARENT_OUTBOUND_CONNECTIONS", "FEATURE_FIRST_PARENT_INBOUND_OUTBOUND_CONNECTIONS", "FEATURE_URL_LENGTH", "FEATURE_AD_KEYWORD", "FEATURE_SPECIAL_CHAR_AD_KEYWORD", "FEATURE_SEMICOLON_PRESENT", "FEATURE_BASE_DOMAIN_IN_QS", "FEATURE_AD_DIMENSIONS_IN_QS", "FEATURE_SCREEN_DIMENSIONS_IN_QS", "FEATURE_AD_DIMENSIONS_IN_COMPLETE_URL", "FEATURE_AVERAGE_DEGREE_CONNECTIVITY", "FEATURE_GRAPH_NODES", "FEATURE_GRAPH_EDGES", "FEATURE_FIRST_PARENT_ASYNC", "FEATURE_FIRST_PARENT_DEFER", "FEATURE_FIRST_PARENT_ATTR_ADDED_BY_SCRIPT", "FEATURE_FIRST_PARENT_ATTR_MODIFIED_BY_SCRIPT", "FEATURE_VALID_QS"]
    ordered_diff = {feat_name: diff[feat_name] for feat_name in specific_order if feat_name in diff}

    return ordered_diff, first_tag


diff, first_tag = compute_diff()
print_dictionary(diff)

fail = 0
idx = 0
domain = ""
url = ""
perturbed_url_file = open('/yopo-artifact/scripts/perturb_html/perturbed_url_{}.csv'.format(attack_option), 'w', newline='')
csv_writer = csv.writer(perturbed_url_file, quoting=csv.QUOTE_MINIMAL, quotechar="'")

with open(target_csv, "r") as f_target:
    domain = ""
    url = ""
    for line in f_target:
        print("@@")
        print(line)
        # for final_domain
        final_domain_with_http, url_num = line.strip().split(",")[:2]
        final_domain = final_domain_with_http.strip().split("://")[-1]
        idx += 1
        print(final_domain_with_http)
        if idx == 1:
            continue
        
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
        prefix = "/".join(final_domain.split("/")[:1]) + "@"
        matching_files = [f for f in os.listdir(mapping_location) if f.startswith(prefix)]
        for match in matching_files:
            with open(mapping_location + "/" + match, "r") as f_domain:
                csv_reader = csv.reader(f_domain)
                for row in csv_reader:
                    if len(row) == 2 and row[0] == url_num:
                        url = row[1]
                        break
        if url == "":
            raise("url not found in the csv file")
        print("requested url: {}".format(url))
        
        # # For test
        # domain = "9to5mac.com"
        # final_domain = "https://9to5mac.com/"
        # url = "https://secure.quantserve.com/quant.js"
        
        # for html, html_fname
        # html, html_fname = read_original_html(domain)
        html, html_fname, candidate_tags, html_content = read_original_html(domain)
        query_strings = get_query_strings_from_html(html_content)

        df_diff = pd.read_csv(delta_csv)
        avg_conn = float(df_diff["FEATURE_AVERAGE_DEGREE_CONNECTIVITY"].values[0])

        
        if avg_conn >= 0: 
            strategy = "Distributed"
        else:
            strategy = "Centralized"
        # strategy = "Centralized"
        print("strategy : {}".format(strategy))
        
        new_html = None
        orig_url = url
        
        diff
        
        # modify html
        try:
            for feature_name, delta in diff.items():
                new_html, modified_url = featureMapbacks(
                    name=feature_name, 
                    html=html, 
                    url=url,
                    first_tag=first_tag,
                    delta=int(delta),
                    domain=final_domain,
                    strategy=strategy,
                    candidate=candidate_tags,
                    qs=query_strings,
                )

                if new_html is None:
                    print("ERROR")
                    continue
                else:
                    html = new_html
                    url = modified_url
        
            with open(MODIFIED_CRAWLED_DIR + "/{}_{}.html".format(domain, url_num), 'w') as f:
                f.write(str(html))
            
            csv_writer.writerow([orig_url, url, "{}_{}.html".format(domain, url_num)])
        
        except Exception as e:
            print(e)
            print("ERRORRRRRRRRRRRRRR!!!!!!!!!!!!")
            fail += 1
            continue
        
print(fail)