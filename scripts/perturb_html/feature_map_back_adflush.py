from bs4 import BeautifulSoup
import math
import csv
import random
from time import sleep
import os
import sys
from tqdm import tqdm
import subprocess
import json
import requests
import re
import pandas as pd
from urllib.parse import urlparse, parse_qs, urlunparse
from perturb_html_adflush import featureMapbacks
import argparse
csv.field_size_limit(sys.maxsize)
sys.path.append('..')
import feature_names_adflush

parser = argparse.ArgumentParser()
parser.add_argument('--attack-option', type=str)
args = parser.parse_args()

attack_option = args.attack_option

BASE_CRAWLED_DIR = "/yopo-artifact/data/rendering_stream/html"
MODIFIED_CRAWLED_DIR = "/yopo-artifact/data/rendering_stream/modified_html_adflush"
JS_SAVED_DIR = "/yopo-artifact/data/rendering_stream/saved_js_adflush"
delta_csv = "/yopo-artifact/data/dataset/delta_nbackdoor_{}.csv".format(attack_option)
target_csv = "/yopo-artifact/data/dataset/from_adflush/target_features_rf_full.csv"
csv_map_local = "/yopo-artifact/data/rendering_stream/map_local_list_unmod_final.csv"

def remove_query_strings(url):
    parsed_url = urlparse(url)
    # Create a new tuple without query strings
    clean_url = urlunparse(parsed_url._replace(query=''))
    clean_url = clean_url.split("#")[0]
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
    response = requests.get(url, timeout=180)
    with open(filename, "wb") as file:
        file.write(response.content)

def treewalk(node):
    ret=[]
    if isinstance(node, list):
        for child in node:
            ret+=treewalk(child)
    elif isinstance(node, dict):
        for key, child in node.items():
            if isinstance(child, (dict, list)):
                ret+=treewalk(child)
        if 'type' in node:
            ret.append(node['type'])
    return ret

def makeAST(filename):
    # read {fname}.js from processing directory, parse AST to .txt in processing directory
    try:
        result=subprocess.check_output('node /yopo-artifact/AdFlush/source/ast_parser.js'+' '+filename+' '+filename+'.txt', shell=True)        
        result=result.decode('UTF8').split()[0]
        if result=='OKAY':
            return 1
        else:
            return 0
    except subprocess.CalledProcessError:
        return -1
    
def count_ngram(filename):
    with open(filename,'r',encoding='UTF8') as readf:
        try:
            source_code=readf.read()
            astresult=makeAST(filename)
            if astresult==1:
                with open(filename +'.txt','r', encoding="UTF8") as astf:
                    parseresult=json.loads(astf.read())
                    ast=parseresult['ast']
                    gram_source=treewalk(ast)
                    with open('/yopo-artifact/AdFlush/source/json/ngram_token_dict.json','r') as asttoken:
                        ast_token_dict=json.loads(asttoken.read())
                        idx_gram_src=[ast_token_dict[t] for t in gram_source]
                        ngram_len=len(idx_gram_src)-2
        except Exception as err:
            print(err)
            ngram_len = 1
    return ngram_len

        
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
        if feat_name in feature_names_adflush.FEATURES_TO_PERTURBE_BINARY:
            value = int(value)
            if value == 0:
                value = -1
            diff.update({feat_name: value})
            
        # handling numerical features
        else:
            value = float(value)
            value = round(value, 10)
            diff.update({feat_name: value})
    
    # handling contradicting perturbation
    # try:
    #     if diff["num_nodes"] <= 0 or diff ["num_edges"] <= 0:
    #         diff["num_nodes"] = 0
    #         diff["num_edges"] = 0
    # except:
    #     pass
    
    # ordering diff
    specific_order = ["keyword_raw_present", "num_get_storage", "num_set_storage", "num_get_cookie", "num_requests_sent", "ng_0_0_2", "ng_0_15_15", "ng_2_13_2", "ng_15_0_3", "ng_15_0_15", "ng_15_15_15", "url_length", "brackettodot", "avg_ident", "avg_charperline"]
    ordered_diff = {feat_name: diff[feat_name] for feat_name in specific_order if feat_name in diff}

    return ordered_diff


diff = compute_diff()
print_dictionary(diff)

fail = 0
idx = 0
domain = ""
filename = ""
url = ""
perturbed_url_file = open('/yopo-artifact/scripts/perturb_html/perturbed_url_{}.csv'.format(attack_option), 'w', newline='')
merged_mapping_file = open("/yopo-artifact/data/rendering_stream/mod_mappings_adflush/merged/url_mappings.csv", 'w', newline='')
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
        # avg_conn = float(df_diff["average_degree_connectivity"].values[0])

        
        # if avg_conn >= 0: 
        #     strategy = "Distributed"
        # else:
        #     strategy = "Centralized"
        strategy = "Centralized"
        print("strategy : {}".format(strategy))
        
        new_html = None
        orig_url = url
        
        if domain in domain_counts:
            domain_counts[domain] += 1
        else:
            domain_counts[domain] = 0
            
        # Save JS url as file
        if is_js_file(orig_url):
            is_JS = True
            filename = JS_SAVED_DIR + "/{}_{}.js".format(domain, domain_counts[domain])
            save_js_file(orig_url, filename)
            # url_without_query = remove_query_strings(orig_url)
            # csv_writer_mapping_merge.writerow([filename, url_without_query])
            ngram_len = count_ngram(filename)

            print(f"JS file '{filename}' saved successfully.")
        else:
            filename = ""
            ngram_len = 1
            print("NOT JS file.")
        
        # modify html
        try:
            for feature_name, delta in diff.items():
                if feature_name.startswith("ng_") or feature_name == "brackettodot" or feature_name == "avg_ident" or feature_name == "avg_charperline":
                    new_html, modified_url = featureMapbacks(
                        name=feature_name, 
                        html=html, 
                        url=url,
                        delta=float(delta),
                        domain=final_domain,
                        strategy=strategy,
                        candidate=candidate_tags,
                        qs=query_strings,
                        _js_fname=filename,
                        ngram_len=ngram_len
                    )
                else:
                    new_html, modified_url = featureMapbacks(
                        name=feature_name, 
                        html=html, 
                        url=url,
                        delta=int(delta),
                        domain=final_domain,
                        strategy=strategy,
                        candidate=candidate_tags,
                        qs=query_strings,
                        _js_fname=filename,
                        ngram_len=ngram_len
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
                url_without_query = remove_query_strings(url)
                csv_writer_mapping_merge.writerow([filename, url_without_query])
                
        
        except Exception as e:
            print(e)
            print("ERRORRRRRRRRRRRRRR!!!!!!!!!!!!")
            fail += 1
            continue
        
print(fail)