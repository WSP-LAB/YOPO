#!/bin/bash
set -e

LOG_DIR="/yopo-artifact/logs"
NUM_CRAWLER=32
monitor_path="/yopo-artifact/scripts/crawler/adgraph/running_check"


echo "[Crawling phase 0] Unzip AdGraph chrome binary..."
unzip /yopo-artifact/A4/AdGraphAPI/AdGraph-Ubuntu-16.04/chrome.zip -d /yopo-artifact/A4/AdGraphAPI/AdGraph-Ubuntu-16.04/
chmod 755 /yopo-artifact/A4/AdGraphAPI/AdGraph-Ubuntu-16.04/chrome

echo "[Crawling phase 1] Generating timeline files using AdGraph binary..."
echo "[Crawling phase 1] Enter 'tmux attach -t crawling' or 'tmux attach -t crawling_python' to see what happens!"
start_time=$(date +%s)

function check_files_exist() {
    for i in {1..10}; do
        if [[ ! -f "${monitor_path}/End_${i}" ]]; then
            return 1
        fi
    done
    return 0
}

# Delete monitoring files
for i in {1..10}; do
    rm -rf "${monitor_path}/End_${i}"
done
rm -rf /root/rendering_stream
sleep 2

# Create new session
tmux new-session -d -s crawling
for i in {1..10}; do
    tmux new-window -t crawling:$i
done

command_proxy="cd /yopo-artifact/mitmproxy && . venv/bin/activate && mitmproxy --map-local-file /yopo-artifact/data/rendering_stream/map_local_list_unmod_final.csv -p"
tmux send-keys -t crawling:1 "${command_proxy} 6666" Enter
tmux send-keys -t crawling:2 "${command_proxy} 6667" Enter
tmux send-keys -t crawling:3 "${command_proxy} 6668" Enter
tmux send-keys -t crawling:4 "${command_proxy} 6669" Enter
tmux send-keys -t crawling:5 "${command_proxy} 6670" Enter
tmux send-keys -t crawling:6 "${command_proxy} 6671" Enter
tmux send-keys -t crawling:7 "${command_proxy} 6672" Enter
tmux send-keys -t crawling:8 "${command_proxy} 6673" Enter
tmux send-keys -t crawling:9 "${command_proxy} 6674" Enter
tmux send-keys -t crawling:10 "${command_proxy} 6675" Enter
# tmux attach-session -t crawling
tmux new-session -d -s crawling_python

for i in {1..10}; do
    tmux new-window -t crawling_python:$i
done

command_python="conda deactivate && conda activate adgraph && python3 /yopo-artifact/scripts/crawler/adgraph/generate_timeline.py --crawler-id"
sleep 3
tmux send-keys -t crawling_python:1 "${command_python} 0" Enter
tmux send-keys -t crawling_python:2 "${command_python} 1" Enter
tmux send-keys -t crawling_python:3 "${command_python} 2" Enter
tmux send-keys -t crawling_python:4 "${command_python} 3" Enter
tmux send-keys -t crawling_python:5 "${command_python} 4" Enter
tmux send-keys -t crawling_python:6 "${command_python} 5" Enter
tmux send-keys -t crawling_python:7 "${command_python} 6" Enter
tmux send-keys -t crawling_python:8 "${command_python} 7" Enter
tmux send-keys -t crawling_python:9 "${command_python} 8" Enter
tmux send-keys -t crawling_python:10 "${command_python} 9" Enter

while true; do
    if check_files_exist; then
        break
    fi
    sleep 20
done

# Kill the existing sessions
tmux kill-session -t crawling
tmux kill-session -t crawling_python


echo "[Crawling phase 2] Parsing timeline files..."
rm -rf /yopo-artifact/data/rendering_stream/timeline
mkdir /yopo-artifact/data/rendering_stream/timeline
mv /root/rendering_stream/* /yopo-artifact/data/rendering_stream/timeline
sleep 3

# We need python2 for parsing
echo "[Crawling phase 2] Now parsing the timeline files... Check parsing.log files!"
source /opt/anaconda/etc/profile.d/conda.sh
conda activate python2
python2 /yopo-artifact/scripts/crawler/adgraph/rules_parsing.py --num-crawler $NUM_CRAWLER > "$LOG_DIR/parsing.log"

echo "[Crawling phase 3] Extracting features for AdGraph..."
rm -rf /yopo-artifact/data/rendering_stream/mappings
rm -rf /yopo-artifact/data/rendering_stream/features
mkdir /yopo-artifact/data/rendering_stream/mappings
mkdir /yopo-artifact/data/rendering_stream/features
sleep 3

source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
echo "[Crawling phase 3] Now extracting the features for adgraph... Check extract_features.log files!"
python3 /yopo-artifact/scripts/crawler/adgraph/extract_features.py --num-crawler $NUM_CRAWLER > "$LOG_DIR/extract_features.log"

echo "[Crawling phase 4] Merging extracted features..."
python3 /yopo-artifact/scripts/crawler/adgraph/merge_features.py

# Identify & exclude non-numeric rows
# This error occurs due to invalid domain name parsing
python3 -c "from utils import delete_invalid_rows; delete_invalid_rows('adgraph')"
# Add test rows for one-hot encoding of binary features
python3 -c "from utils import add_test_rows; add_test_rows('adgraph')"

echo "[Crawling phase 5] Preprocessing data and select target request candidates..."
python3 /yopo-artifact/scripts/crawler/adgraph/preprocessing_RF.py
python3 /yopo-artifact/scripts/crawler/adgraph/preprocessing_NN.py

echo "[Crawling phase 6] Verifying target request candidates and select 2K target requests..."
echo "[Crawling phase 6] Now verifying the target requests... Check verify_target_requests.log files!"
source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
python3 /yopo-artifact/scripts/crawler/adgraph/verify_target_requests.py --target-blocker adgraph --oversampled > "$LOG_DIR/verify_target_requests_oversampled_adgraph.log"

echo "[Crawling phase 7] Generating mod_mappings files..."
rm -rf /yopo-artifact/data/rendering_stream/modified_html_adgraph
mkdir /yopo-artifact/data/rendering_stream/modified_html_adgraph
rm -rf /yopo-artifact/data/rendering_stream/mod_mappings_adgraph
mkdir /yopo-artifact/data/rendering_stream/mod_mappings_adgraph
cp /yopo-artifact/data/rendering_stream/map_local_list_unmod_final.csv /yopo-artifact/data/rendering_stream/map_local_list_mod_final.csv
sed -i "s/rendering_stream\/html/rendering_stream\/modified_html/g" "/yopo-artifact/data/rendering_stream/map_local_list_mod_final.csv"
python3 /yopo-artifact/scripts/crawler/adgraph/verify_target_requests.py --target-blocker adgraph > "$LOG_DIR/verify_target_requests_adgraph.log"
python3 /yopo-artifact/scripts/crawler/adgraph/generate_mod_mappings.py > "$LOG_DIR/generate_mod_mappings_adgraph.log"

# Delete test rows for one-hot encoding of binary features
python3 -c "from utils import delete_test_rows; delete_test_rows('adgraph')"
