#!/bin/bash
set -e

generate_UAP() {
    python3 UAP_implement.py --csv-path $1 --csv-name-ad $2 --out-name $3 --delta-name $4 --model-fpath $5 --csv-target-name $6 --lagrangain $7 --sampling-size $8 --epsilon $9 --mode ${10} --cuda ${11}
}

test_UAP() {
    python3 test_ASR_webgraph.py --csv-path $1 --csv-name-before-attack $2 --csv-name-final $3 --model-fpath $4 --attack-option $5
}

mode="webgraph"
perc="30"
query_size="100000"
option="${perc}perc_${query_size}"
sampling_size="40000"
lagrangain="400"
attack_option="${perc}perc_inv${sampling_size}_query_${query_size}_lag_${lagrangain}_eps${epsilon}_${cost_type}_webgraph"
map_count=$(ls /yopo-artifact/data/rendering_stream/mod_mappings_webgraph/map_mod_* | wc -l)
LOG_DIR="/yopo-artifact/logs"
cuda="0"


echo "[Phase 2-1] generate a UAP for WebGraph..."
source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
generate_UAP /yopo-artifact/data/dataset/ final_${option}_for_inversion_webgraph.csv perturbed_features_nbackdoor_${attack_option}.csv /delta_nbackdoor_${attack_option}.csv /yopo-artifact/data/dataset/from_webgraph/saved_model_webgraph/surrogate_${option}_weighted.pt from_webgraph/target_features_rf.csv $lagrangain $sampling_size $epsilon $mode $cuda
conda deactivate

echo "[Phase 2-2] generate perturbed HTML for WebGraph..."
sleep 5
rm -rf /yopo-artifact/data/rendering_stream/modified_html_webgraph
rm -rf /yopo-artifact/data/rendering_stream/saved_js
rm -rf /yopo-artifact/data/rendering_stream/mod_mappings_webgraph/merged
mkdir /yopo-artifact/data/rendering_stream/modified_html_webgraph
mkdir /yopo-artifact/data/rendering_stream/saved_js
mkdir /yopo-artifact/data/rendering_stream/mod_mappings_webgraph/merged

source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
cd /yopo-artifact/scripts/perturb_html
python3 /yopo-artifact/scripts/perturb_html/feature_map_back_webgraph.py --attack-option ${attack_option} > "$LOG_DIR/perturb_html_webgraph.log"

echo "[Phase 2-3] Crawling modified websites for WebGraph... Total map_count: $map_count"
rm -rf /yopo-artifact/OpenWPM/datadir_proxy_webgraph
rm -rf /yopo-artifact/scripts/perturb_html/running_check_webgraph
mkdir /yopo-artifact/OpenWPM/datadir_proxy_webgraph
mkdir /yopo-artifact/OpenWPM/datadir_proxy_webgraph/content_dir
mkdir /yopo-artifact/OpenWPM/datadir_proxy_webgraph/crawl_dir
mkdir /yopo-artifact/OpenWPM/datadir_proxy_webgraph/log_dir
mkdir /yopo-artifact/OpenWPM/datadir_proxy_webgraph/screenshots
mkdir /yopo-artifact/OpenWPM/datadir_proxy_webgraph/sources
mkdir /yopo-artifact/scripts/perturb_html/running_check_webgraph

monitor_path="/yopo-artifact/scripts/perturb_html/running_check_webgraph"

function check_files_exist() {
    for i in {1..16}; do
        if [[ ! -f "${monitor_path}/End_${i}" ]]; then
            return 1
        fi
    done
    return 0
}

# Iterate mapping crawling
for map_idx in $(seq 0 $((map_count - 1))); do
    echo "Current map_idx: $map_idx"
    start_time=$(date +%s)

    # Delete monitoring files
    for i in {1..16}; do
        rm -rf "${monitor_path}/End_${i}"
    done
    sleep 3
    
    # Create new session
    tmux new-session -d -s crawling_modification_webgraph

    for i in {1..16}; do
        tmux new-window -t crawling_modification_webgraph:$i
    done

    python3 /yopo-artifact/scripts/perturb_html/merge_mod_mappings_webgraph.py --map-idx ${map_idx}

    command_proxy="cd /yopo-artifact/mitmproxy && . venv/bin/activate && mitmproxy --map-local-file /yopo-artifact/data/rendering_stream/mod_mappings_webgraph/merged/merged_map_mod_${map_idx}.csv -p"
    echo "mapping command: $command_proxy"

    cd /yopo-artifact/mitmproxy

    tmux send-keys -t crawling_modification_webgraph:1 "${command_proxy} 6766" Enter
    tmux send-keys -t crawling_modification_webgraph:2 "${command_proxy} 6767" Enter
    tmux send-keys -t crawling_modification_webgraph:3 "${command_proxy} 6768" Enter
    tmux send-keys -t crawling_modification_webgraph:4 "${command_proxy} 6769" Enter
    tmux send-keys -t crawling_modification_webgraph:5 "${command_proxy} 6770" Enter
    tmux send-keys -t crawling_modification_webgraph:6 "${command_proxy} 6771" Enter
    tmux send-keys -t crawling_modification_webgraph:7 "${command_proxy} 6772" Enter
    tmux send-keys -t crawling_modification_webgraph:8 "${command_proxy} 6773" Enter
    tmux send-keys -t crawling_modification_webgraph:9 "${command_proxy} 6774" Enter
    tmux send-keys -t crawling_modification_webgraph:10 "${command_proxy} 6775" Enter
    tmux send-keys -t crawling_modification_webgraph:11 "${command_proxy} 6776" Enter
    tmux send-keys -t crawling_modification_webgraph:12 "${command_proxy} 6777" Enter
    tmux send-keys -t crawling_modification_webgraph:13 "${command_proxy} 6778" Enter
    tmux send-keys -t crawling_modification_webgraph:14 "${command_proxy} 6779" Enter
    tmux send-keys -t crawling_modification_webgraph:15 "${command_proxy} 6780" Enter
    tmux send-keys -t crawling_modification_webgraph:16 "${command_proxy} 6781" Enter

    tmux new-session -d -s crawling_modification_python_webgraph
    for i in {1..16}; do
        tmux new-window -t crawling_modification_python_webgraph:$i
    done

    command_python="conda deactivate && conda activate openwpm && python3 /yopo-artifact/OpenWPM/demo_proxy_auto_webgraph.py --mapping-id ${map_idx} --crawler-id"
    echo "crawling command: $command_python"

    cd /yopo-artifact/mitmproxy

    sleep 5

    tmux send-keys -t crawling_modification_python_webgraph:1 "${command_python} 0" Enter
    tmux send-keys -t crawling_modification_python_webgraph:2 "${command_python} 1" Enter
    tmux send-keys -t crawling_modification_python_webgraph:3 "${command_python} 2" Enter
    tmux send-keys -t crawling_modification_python_webgraph:4 "${command_python} 3" Enter
    tmux send-keys -t crawling_modification_python_webgraph:5 "${command_python} 4" Enter
    tmux send-keys -t crawling_modification_python_webgraph:6 "${command_python} 5" Enter
    tmux send-keys -t crawling_modification_python_webgraph:7 "${command_python} 6" Enter
    tmux send-keys -t crawling_modification_python_webgraph:8 "${command_python} 7" Enter
    tmux send-keys -t crawling_modification_python_webgraph:9 "${command_python} 8" Enter
    tmux send-keys -t crawling_modification_python_webgraph:10 "${command_python} 9" Enter
    tmux send-keys -t crawling_modification_python_webgraph:11 "${command_python} 10" Enter
    tmux send-keys -t crawling_modification_python_webgraph:12 "${command_python} 11" Enter
    tmux send-keys -t crawling_modification_python_webgraph:13 "${command_python} 12" Enter
    tmux send-keys -t crawling_modification_python_webgraph:14 "${command_python} 13" Enter
    tmux send-keys -t crawling_modification_python_webgraph:15 "${command_python} 14" Enter
    tmux send-keys -t crawling_modification_python_webgraph:16 "${command_python} 15" Enter

    while true; do
        if check_files_exist; then
            break
        fi
        sleep 10
    done

    # Kill the existing sessions
    tmux kill-session -t crawling_modification_webgraph
    tmux kill-session -t crawling_modification_python_webgraph

    end_time=$(date +%s)
    total_time=$((end_time - start_time))
    
    echo "mapping $map_idx running time: $total_time seconds"
    sleep 10
done

echo "[Phase 2-4] Extract features for WebGraph..."
sleep 10
rm -rf /yopo-artifact/WebGraph/result
cd /yopo-artifact/WebGraph

source /opt/anaconda/etc/profile.d/conda.sh
conda activate openwpm
python code/run_automate.py

echo "[Phase 2-5] merge features for WebGraph..."
python3 code/my_utils.py

echo "[Phase 2-6] extract features..."
source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
python3 /yopo-artifact/scripts/crawler/webgraph/filter_target_for_attack.py --attack-option ${attack_option}

echo "[Phase 2-7] re-preprocess for WebGraph..."
source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
python3 /yopo-artifact/scripts/crawler/webgraph/preprocessing_RF_for_attack.py --attack-option ${attack_option}

echo "[Phase 2-8] compute ASR for WebGraph..."
cd /yopo-artifact/scripts
test_UAP /yopo-artifact/data/dataset/ from_webgraph/target_features_rf.csv from_webgraph/modified_features_target_rf_decoded_drop_webgraph_${attack_option}.csv /yopo-artifact/data/dataset/from_webgraph/saved_model_webgraph/rf_model_30perc.pt ${attack_option}
