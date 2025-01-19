#!/bin/bash
set -e

LOG_DIR="/yopo-artifact/logs"
NUM_CRAWLER=32

echo "[Crawling phase 1] Generating mapping files..."
source /yopo-artifact/PageGraph/pagegraph-query/venv/bin/activate
cd /yopo-artifact/PageGraph/pagegraph-query
python rewrite.py --mapping_path /yopo-artifact/data/rendering_stream/map_local_list_unmod_final.csv --html_path /yopo-artifact/data/rendering_stream/html

echo "[Crawling phase 2] Turning on mitmproxy..."
cd /yopo-artifact/mitmproxy
./run_for_pagegraph.sh $NUM_CRAWLER /yopo-artifact/PageGraph/pagegraph-query/final_url_to_modified_html_filepath_mapping_AE.csv

echo "[Crawling phase 3] Building PageGraph..."
rm -rf /yopo-artifact/data/rendering_stream/pagegraph/*
cd /yopo-artifact/PageGraph/pagegraph-crawl
npm install argparse
python build_pagegraph.py --map-local-file /yopo-artifact/PageGraph/pagegraph-query/final_url_to_modified_html_filepath_mapping_AE.csv -b /usr/bin/brave-browser -o /yopo-artifact/data/rendering_stream/pagegraph -j $NUM_CRAWLER -t 600
rm -rf /tmp/pagegraph-profile--*
tmux kill-server

echo "[Crawling phase 4] Extracting features from PageGraph..."
source /yopo-artifact/PageGraph/pagegraph-query/venv/bin/activate
cd /yopo-artifact/PageGraph/pagegraph-query
rm -rf /yopo-artifact/data/rendering_stream/features_pagegraph
mkdir /yopo-artifact/data/rendering_stream/features_pagegraph
python extract_features.py --graph_dir /yopo-artifact/data/rendering_stream/pagegraph --feature_dir /yopo-artifact/data/rendering_stream/features_pagegraph --mapping_path /yopo-artifact/PageGraph/pagegraph-query/final_url_to_modified_html_filepath_mapping_AE.csv -j $NUM_CRAWLER -t 600

echo "[Crawling phase 5] Merging extracted features..."
cd /yopo-artifact/scripts/crawler
python3 -c "from utils import merging_unmod_pagegraph; merging_unmod_pagegraph()"

echo "[Crawling phase 5] Labelling merged features..."
source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
python3 /yopo-artifact/scripts/crawler/pagegraph/label_features.py

# Add test rows for one-hot encoding of binary features
python3 -c "from utils import add_test_rows; add_test_rows('pagegraph')"

echo "[Crawling phase 6] Preprocessing data and select target request candidates..."
python3 /yopo-artifact/scripts/crawler/pagegraph/preprocessing_RF.py
python3 /yopo-artifact/scripts/crawler/pagegraph/preprocessing_NN.py

echo "[Crawling phase 7] Verifying target request candidates and select 2K target requests..."
echo "[Crawling phase 7] Now verifying the target requests... Check verify_target_requests_pagegraph.log files!"
source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
python3 /yopo-artifact/scripts/crawler/pagegraph/verify_target_requests.py --target-blocker pagegraph --oversampled > "$LOG_DIR/verify_target_requests_oversampled_pagegraph.log"

# Delete test rows for one-hot encoding of binary features
python3 -c "from utils import delete_test_rows; delete_test_rows('pagegraph')"
