from bs4 import BeautifulSoup
import math
import csv
import os
import sys
import pandas as pd
csv.field_size_limit(sys.maxsize)
from perturb_html_for_verifying import featureMapbacks
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--target-blocker", type=str)
parser.add_argument("--oversampled", action='store_true')
args = parser.parse_args()

if args.oversampled:
    target_csv = "/yopo-artifact/data/dataset/from_adflush/target_features_rf_oversampled.csv"
else:
    target_csv = "/yopo-artifact/data/dataset/from_adflush/target_features_rf_full.csv"
print(target_csv)

BASE_CRAWLED_DIR = "/yopo-artifact/data/rendering_stream/html"
MODIFIED_CRAWLED_DIR = "/yopo-artifact/data/rendering_stream/modified_html_adflush"
# mapping_location = "/yopo-artifact/data/rendering_stream/mappings"
csv_map_local = "/yopo-artifact/data/rendering_stream/map_local_list_unmod_final.csv"

def print_dictionary(dictionary):
    print("---------- Diff value ----------")
    for key, value in dictionary.items():
        print("{}: {}".format(key, value))
    print("--------------------------------")

def read_original_html(domain):
    print("Reading HTML: {}".format(domain))
    with open(BASE_CRAWLED_DIR + "/" + domain + '.html', "r") as fin:
        curr_html = BeautifulSoup(fin, features="html.parser")
    
    return curr_html, domain + '.html'

def compute_diff():
    diff = dict()
    diff = {"semicolon_in_query": 1, "url_length": 5}

    # # find tag names
    # # Only for adgraph
    # first_tag = "1"
    
    # ordering diff
    # specific_order = ["FEATURE_URL_LENGTH", "FEATURE_SEMICOLON_IN_QUERY", "FEATURE_FIRST_PARENT_TAG_NAME", "FEATURE_FIRST_NUMBER_OF_SIBLINGS", "FEATURE_FIRST_PARENT_NUMBER_OF_SIBLINGS", "FEATURE_FIRST_PARENT_SIBLING_AD_ATTRIBUTE", "FEATURE_FIRST_PARENT_INBOUND_CONNECTIONS", "FEATURE_FIRST_PARENT_OUTBOUND_CONNECTIONS", "FEATURE_FIRST_PARENT_INBOUND_OUTBOUND_CONNECTIONS", "FEATURE_URL_LENGTH", "FEATURE_AD_KEYWORD", "FEATURE_SPECIAL_CHAR_AD_KEYWORD", "FEATURE_SEMICOLON_PRESENT", "FEATURE_BASE_DOMAIN_IN_QS", "FEATURE_AD_DIMENSIONS_IN_QS", "FEATURE_SCREEN_DIMENSIONS_IN_QS", "FEATURE_AD_DIMENSIONS_IN_COMPLETE_URL", "FEATURE_AVERAGE_DEGREE_CONNECTIVITY", "FEATURE_GRAPH_NODES", "FEATURE_GRAPH_EDGES", "FEATURE_FIRST_PARENT_ASYNC", "FEATURE_FIRST_PARENT_DEFER", "FEATURE_FIRST_PARENT_ATTR_ADDED_BY_SCRIPT", "FEATURE_FIRST_PARENT_ATTR_MODIFIED_BY_SCRIPT"]
    # specific_order = ["in_out_degree", "ascendant_has_ad_keyword", "url_length", "keyword_raw_present", "keyword_char_present", "semicolon_in_query", "base_domain_in_query", "ad_size_in_qs_present", "screen_size_present", "ad_size_present", "average_degree_connectivity", "num_nodes", "num_edges","num_get_cookie", "num_set_cookie","num_set_storage","num_get_storage"]
    specific_order = ["keyword_raw_present", "num_get_storage", "num_set_storage", "num_get_cookie", "num_requests_sent", "ng_0_0_2", "ng_0_15_15", "ng_2_13_2", "ng_15_0_3", "ng_15_0_15", "ng_15_15_15", "url_length", "brackettodot", "avg_ident", "avg_charperline"]
    ordered_diff = {feat_name: diff[feat_name] for feat_name in specific_order if feat_name in diff}

    # return ordered_diff, first_tag
    return ordered_diff

# # for adgraph
# diff, first_tag = compute_diff()

# for webgraph
diff = compute_diff()

print_dictionary(diff)

fail = 0
idx = 0
domain = ""
url = ""
perturbed_url_file = open('/yopo-artifact/scripts/crawler/adflush/perturbed_url_for_target_adflush.csv', 'w', newline='')
csv_writer = csv.writer(perturbed_url_file, quoting=csv.QUOTE_MINIMAL, quotechar="'")
header = ['1', '2', '3']
csv_writer.writerow(header)

domain_counts = {}

with open(target_csv, "r") as f_target:
    domain = ""
    url = ""
    for line in f_target:
        # for final_domain
        
        # # adgraph
        # final_domain_with_http, url_num = line.strip().split(",")[:2]
        # final_domain = final_domain_with_http.strip().split("://")[-1]
        
        # webgraph
        final_domain_with_http= line.strip().split(",")[0]
        final_domain = final_domain_with_http.strip().split("://")[-1]
        url = line.split(",")[2]
        
        idx += 1
        if idx == 1:
            continue
        
        # for domain
        with open(csv_map_local, "r") as f_map:
            csv_reader = csv.reader(f_map)
            for row in csv_reader:
                # print(row)
                if row[1] == final_domain_with_http:
                    file_path = row[0]
                    file_name = file_path.split("/")[-1]
                    domain = ".".join(file_name.split(".")[:-1])
                    break
            if domain == "":
                raise("domain not found in the CSV file.")
        
        # for url
        
        # # adgraph
        # print("Final Domain: {}".format(final_domain))
        # print("Domain: {}".format(domain))
        # prefix = "/".join(final_domain.split("/")[:1]) + "@"
        # matching_files = [f for f in os.listdir(mapping_location) if f.startswith(prefix)]
        # for match in matching_files:
        #     with open(mapping_location + "/" + match, "r") as f_domain:
        #         csv_reader = csv.reader(f_domain)
        #         for row in csv_reader:
        #             if len(row) == 2 and row[0] == url_num:
        #                 url = row[1]
        #                 break
        
        # webgraph
        print("Final Domain: {}".format(final_domain))
        print("Domain: {}".format(domain))
        print("Requested URL: {}".format(url))
        
        if url == "":
            raise("url not found in the csv file")
        print("requested url: {}".format(url))
        
        # for html, html_fname
        html, html_fname = read_original_html(domain)
        
        # # for adgraph
        # avg_conn = 1

        strategy = "Centralized"
        new_html = None
        orig_url = url
        
        # webgraph
        if domain in domain_counts:
            domain_counts[domain] += 1
        else:
            domain_counts[domain] = 0
        
        # modify html
        # # adgraph
        # try:
        #     for feature_name, delta in diff.items():
        #         new_html, modified_url = featureMapbacks(
        #             name=feature_name, 
        #             html=html, 
        #             url=url,
        #             first_tag=first_tag,
        #             delta=int(delta),
        #             domain=final_domain,
        #             strategy=strategy,
        #         )
        
        # webgraph
        try:
            for feature_name, delta in diff.items():
                new_html, modified_url = featureMapbacks(
                    name=feature_name, 
                    html=html, 
                    url=url,
                    delta=int(delta),
                    domain=final_domain,
                    strategy=strategy,
                    js_fname="a"
                )


                if new_html is None:
                    print("ERROR")
                    continue
                else:
                    html = new_html
                    url = modified_url

            if not args.oversampled:
                # with open(MODIFIED_CRAWLED_DIR + "/{}_{}.html".format(domain, url_num), 'w') as f:
                #     f.write(str(html))
                with open(MODIFIED_CRAWLED_DIR + "/{}_{}.html".format(domain, domain_counts[domain]), 'w') as f:
                    f.write(str(html))

            # # adgraph        
            # csv_writer.writerow([orig_url, url, "{}_{}.html".format(domain, url_num)])
            
            # webgraph            
            csv_writer.writerow([orig_url, url, "{}_{}.html".format(domain, domain_counts[domain])])
        
        except Exception as e:
            print(e)
            print("ERRORRRRRRRRRRRRRR!!!!!!!!!!!!")
            fail += 1
            
            # csv_writer.writerow([orig_url, url, "{}_{}.html".format(domain, url_num)])
            csv_writer.writerow([orig_url, url, "{}_{}.html".format(domain, domain_counts[domain])])
            continue
        
perturbed_url_file.close()

if args.oversampled:
    # Filtering 2K target requests
    target_blocker = args.target_blocker
    df1 = pd.read_csv('/yopo-artifact/scripts/crawler/{}/perturbed_url_for_target_{}.csv'.format(target_blocker, target_blocker))
    filtered_indices = df1[df1.iloc[:, 1].str.endswith("#####")].index[:2000]

    # Read the second CSV file and keep only the rows corresponding to the filtered indices
    df_oversampled = pd.read_csv('/yopo-artifact/data/dataset/from_adflush/target_features_rf_oversampled.csv')
    filtered_df = df_oversampled.iloc[filtered_indices]
    filtered_df.to_csv('/yopo-artifact/data/dataset/from_adflush/target_features_rf_full.csv', index=False)

    # Exclude unnecessary columns
    # col_exclude = ["DOMAIN_NAME", "NODE_ID", "FEATURE_KATZ_CENTRALITY", "FEATURE_FIRST_PARENT_KATZ_CENTRALITY", "FEATURE_SECOND_PARENT_KATZ_CENTRALITY"]
    col_exclude = ["top_level_url", "visit_id", "name"]
    filtered_df_excluded = filtered_df.drop(columns=col_exclude)

    filtered_df_excluded.to_csv('/yopo-artifact/data/dataset/from_adflush/target_features_rf.csv', index=False)