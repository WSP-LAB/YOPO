#!/bin/bash
set -e

LOG_DIR="/yopo-artifact/logs"

# +-----------------------------------------------------------+
# |  Please run webgraph crawler (crawl_webgraph.sh) first!!  |
# +-----------------------------------------------------------+

# Add test rows for one-hot encoding of binary features
python3 -c "from utils import add_test_rows; add_test_rows('adflush')"

# Assume that you have completed to [crawling Phase 3] of the webgraph.
echo "[Crawling phase 4] Extracting AdFlush features..."
python3 -c "from utils import delte_flow_from_features; delte_flow_from_features()"
rm -rf /yopo-artifact/AdFlush/source/MY_jsfile
mkdir /yopo-artifact/AdFlush/source/MY_jsfile
rm -rf /yopo-artifact/data/dataset/from_adflush/*
source /opt/anaconda/etc/profile.d/conda.sh
conda activate adflush
cd /yopo-artifact/AdFlush/source
python3 MY_embedding.py

# Merge crawled adflush dataset
cd /yopo-artifact/scripts/crawler
python3 -c "from utils import merging_unmod_adflush; merging_unmod_adflush()"
python3 -c "from utils import sampling_column_adflush; sampling_column_adflush()"
rm -rf /yopo-artifact/data/dataset/from_adflush/features_raw_*

echo "[Crawling phase 5] Preprocessing data and select target request candidates..."
python3 /yopo-artifact/scripts/crawler/adflush/preprocessing_RF.py
python3 /yopo-artifact/scripts/crawler/adflush/preprocessing_NN.py

echo "[Crawling phase 6] Verifying target request candidates and select 2K target requests..."
echo "[Crawling phase 6] Now verifying the target requests... Check verify_target_requests_adflush.log files!"
source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
python3 /yopo-artifact/scripts/crawler/adflush/verify_target_requests.py --target-blocker adflush --oversampled > "$LOG_DIR/verify_target_requests_oversampled_adflush.log"

echo "[Crawling phase 7] Generating mod_mappings files..."
rm -rf /yopo-artifact/data/rendering_stream/modified_html_adflush
mkdir /yopo-artifact/data/rendering_stream/modified_html_adflush
rm -rf /yopo-artifact/data/rendering_stream/mod_mappings_adflush
mkdir /yopo-artifact/data/rendering_stream/mod_mappings_adflush
cp /yopo-artifact/data/rendering_stream/map_local_list_unmod_final.csv /yopo-artifact/data/rendering_stream/map_local_list_mod_final.csv
sed -i "s/rendering_stream\/html/rendering_stream\/modified_html/g" "/yopo-artifact/data/rendering_stream/map_local_list_mod_final.csv"
python3 /yopo-artifact/scripts/crawler/adflush/verify_target_requests.py --target-blocker adflush > "$LOG_DIR/verify_target_requests_adflush.log"
python3 /yopo-artifact/scripts/crawler/adflush/generate_mod_mappings.py > "$LOG_DIR/generate_mod_mappings_adflush.log"

# Delete test rows for one-hot encoding of binary features
python3 -c "from utils import delete_test_rows; delete_test_rows('adflush')"