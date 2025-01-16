from tqdm import tqdm
from multiprocessing import Pool
from adblockparser import AdblockRules
import argparse
import pandas as pd
import os


parser = argparse.ArgumentParser()
parser.add_argument("--num-crawler", type=int, default='32')
args = parser.parse_args()


def load_filter_lists(directory):
    rules = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r') as f:
                rules.extend(f.readlines())
    return rules


def classify_url(url):
    if rules.should_block(url):
        return 'AD'
    else:
        return 'NONAD'


def classify_chunk(chunk):
    chunk['CLASS'] = chunk['NETWORK_REQUEST_URL'].apply(classify_url)
    return chunk


def labelling_unmod_pagegraph(num_crawler):
    global rules

    filterlist_dir = '/yopo-artifact/data/rendering_stream/filterlists_webgraph'
    adblock_rules = load_filter_lists(filterlist_dir)
    rules = AdblockRules(adblock_rules)

    df = pd.read_csv('/yopo-artifact/data/dataset/from_pagegraph/features_raw_without_label.csv')
    chunk_size = len(df) // num_crawler
    chunks = [df.iloc[i:i + chunk_size] for i in range(0, len(df), chunk_size)]

    tqdm.pandas(desc="Classifying URLs")
    with Pool(num_crawler) as pool:
        results = list(tqdm(pool.imap(classify_chunk, chunks), total=len(chunks), desc="Finished crawlers"))

    labeled_df = pd.concat(results, ignore_index=True)

    # Save
    labeled_df.to_csv('/yopo-artifact/data/dataset/from_pagegraph/features_raw.csv', index=False)

rules = None
labelling_unmod_pagegraph(args.num_crawler)