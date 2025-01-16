#!/bin/bash
set -e

LOG_DIR="/yopo-artifact/logs"

echo "[Crawling phase 0] Unzip firefox requirements..."
unzip /yopo-artifact/OpenWPM/firefox-bin/libxul.so.zip -d /yopo-artifact/OpenWPM/firefox-bin/

echo "[Crawling phase 1] Crawling websites using OpenWPM..."
echo "[Crawling phase 1] Enter 'tmux attach -t crawling_webgraph' or check crawl_webgraph.log files to see what happens!"
source /opt/anaconda/etc/profile.d/conda.sh
conda activate openwpm
rm -rf /yopo-artifact/OpenWPM/datadir_proxy_unmod
mkdir /yopo-artifact/OpenWPM/datadir_proxy_unmod
mkdir /yopo-artifact/OpenWPM/datadir_proxy_unmod/content_dir
mkdir /yopo-artifact/OpenWPM/datadir_proxy_unmod/crawl_dir
mkdir /yopo-artifact/OpenWPM/datadir_proxy_unmod/log_dir

# Create new session
tmux new-session -d -s crawling_webgraph
for i in {1..16}; do
    tmux new-window -t crawling_webgraph:$i
done

command_proxy="cd /yopo-artifact/mitmproxy && . venv/bin/activate && mitmproxy --map-local-file /yopo-artifact/data/rendering_stream/map_local_list_unmod_final.csv -p"
tmux send-keys -t crawling_webgraph:1 "${command_proxy} 5555" Enter
tmux send-keys -t crawling_webgraph:2 "${command_proxy} 5556" Enter
tmux send-keys -t crawling_webgraph:3 "${command_proxy} 5557" Enter
tmux send-keys -t crawling_webgraph:4 "${command_proxy} 5558" Enter
tmux send-keys -t crawling_webgraph:5 "${command_proxy} 5559" Enter
tmux send-keys -t crawling_webgraph:6 "${command_proxy} 5560" Enter
tmux send-keys -t crawling_webgraph:7 "${command_proxy} 5561" Enter
tmux send-keys -t crawling_webgraph:8 "${command_proxy} 5562" Enter
tmux send-keys -t crawling_webgraph:9 "${command_proxy} 5563" Enter
tmux send-keys -t crawling_webgraph:10 "${command_proxy} 5564" Enter
tmux send-keys -t crawling_webgraph:11 "${command_proxy} 5565" Enter
tmux send-keys -t crawling_webgraph:12 "${command_proxy} 5566" Enter
tmux send-keys -t crawling_webgraph:13 "${command_proxy} 5567" Enter
tmux send-keys -t crawling_webgraph:14 "${command_proxy} 5568" Enter
tmux send-keys -t crawling_webgraph:15 "${command_proxy} 5569" Enter
tmux send-keys -t crawling_webgraph:16 "${command_proxy} 5570" Enter
# tmux attach-session -t crawling_webgraph
sleep 5

# Crawling
python3 /yopo-artifact/OpenWPM/demo_proxy.py > "$LOG_DIR/crawl_webgraph.log" 2>&1

# Kill the existing sessions
tmux kill-session -t crawling_webgraph


echo "[Crawling phase 2] Building webgraph..."
source /opt/anaconda/etc/profile.d/conda.sh
conda activate openwpm
rm -rf /yopo-artifact/WebGraph/result_webgraph_unmod
mkdir /yopo-artifact/WebGraph/result_webgraph_unmod

echo "[Crawling phase 3] Merging and labelling..."
python3 /yopo-artifact/WebGraph/code/run_automate_unmod.py
python3 -c "from utils import merging_unmod_webgraph; merging_unmod_webgraph()"
python3 -c "from utils import labelling_unmod_webgraph; labelling_unmod_webgraph()"

# Add test rows for one-hot encoding of binary features
python3 -c "from utils import add_test_rows; add_test_rows('webgraph')"

source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
echo "[Crawling phase 4] Preprocessing data and select target request candidates..."
python3 /yopo-artifact/scripts/crawler/webgraph/preprocessing_RF.py
python3 /yopo-artifact/scripts/crawler/webgraph/preprocessing_NN.py

echo "[Crawling phase 5] Verifying target request candidates and select 2K target requests..."
echo "[Crawling phase 5] Now verifying the target requests... Check verify_target_requests_webgraph.log files!"
python3 /yopo-artifact/scripts/crawler/webgraph/verify_target_requests.py --target-blocker webgraph --oversampled > "$LOG_DIR/verify_target_requests_oversampled_webgraph.log"

echo "[Crawling phase 6] Generating mod_mappings files..."
rm -rf /yopo-artifact/data/rendering_stream/modified_html_webgraph
mkdir /yopo-artifact/data/rendering_stream/modified_html_webgraph
rm -rf /yopo-artifact/data/rendering_stream/mod_mappings_webgraph
mkdir /yopo-artifact/data/rendering_stream/mod_mappings_webgraph
cp /yopo-artifact/data/rendering_stream/map_local_list_unmod_final.csv /yopo-artifact/data/rendering_stream/map_local_list_mod_final.csv
sed -i "s/rendering_stream\/html/rendering_stream\/modified_html/g" "/yopo-artifact/data/rendering_stream/map_local_list_mod_final.csv"
python3 /yopo-artifact/scripts/crawler/webgraph/verify_target_requests.py --target-blocker webgraph > "$LOG_DIR/verify_target_requests_webgraph.log"
python3 /yopo-artifact/scripts/crawler/webgraph/generate_mod_mappings.py > "$LOG_DIR/generate_mod_mappings_webgraph.log"

# Delete test rows for one-hot encoding of binary features
python3 -c "from utils import delete_test_rows; delete_test_rows('webgraph')"
