#!/bin/bash
set -e

generate_UAP() {
    python3 UAP_implement.py --csv-path $1 --csv-name-ad $2 --out-name $3 --delta-name $4 --model-fpath $5 --csv-target-name $6 --lagrangain $7 --sampling-size $8 --epsilon $9 --mode ${10} --cuda ${11}
}

test_UAP() {
    python3 test_ASR_adflush.py --csv-path $1 --csv-name-before-attack $2 --csv-name-final $3 --model-fpath $4 --attack-option $5
}

mode="adflush"
perc="30"
query_size="100000"
option="${perc}perc_${query_size}"
sampling_size="40000"
lagrangain="400"
attack_option="${perc}perc_inv${sampling_size}_query_${query_size}_lag_${lagrangain}_eps${epsilon}_${cost_type}_adflush"
map_count=$(ls /yopo-artifact/data/rendering_stream/mod_mappings_adflush/map_mod_* | wc -l)
LOG_DIR="/yopo-artifact/logs"
cuda="0"


echo "[Phase 2-1] generate a UAP for AdFlush..."
source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
generate_UAP /yopo-artifact/data/dataset/ final_${option}_for_inversion_adflush.csv perturbed_features_nbackdoor_${attack_option}.csv /delta_nbackdoor_${attack_option}.csv /yopo-artifact/data/dataset/from_adflush/saved_model_adflush/surrogate_${option}_weighted.pt from_adflush/target_features_rf.csv $lagrangain $sampling_size $epsilon $mode $cuda
conda deactivate

echo "[Phase 2-2] generate perturbed HTML for AdFlush..."
sleep 5
rm -rf /yopo-artifact/data/rendering_stream/modified_html_adflush
rm -rf /yopo-artifact/data/rendering_stream/saved_js_adflush
rm -rf /yopo-artifact/data/rendering_stream/mod_mappings_adflush/merged
mkdir /yopo-artifact/data/rendering_stream/modified_html_adflush
mkdir /yopo-artifact/data/rendering_stream/saved_js_adflush
mkdir /yopo-artifact/data/rendering_stream/mod_mappings_adflush/merged

source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
cd /yopo-artifact/scripts/perturb_html
python3 /yopo-artifact/scripts/perturb_html/feature_map_back_adflush.py --attack-option ${attack_option} > "$LOG_DIR/perturb_html_adflush.log"

echo "[Phase 2-3] Crawling modified websites for AdFlush... Total map_count: $map_count"
rm -rf /yopo-artifact/OpenWPM/datadir_proxy_adflush
rm -rf /yopo-artifact/scripts/perturb_html/running_check_adflush
mkdir /yopo-artifact/OpenWPM/datadir_proxy_adflush
mkdir /yopo-artifact/OpenWPM/datadir_proxy_adflush/content_dir
mkdir /yopo-artifact/OpenWPM/datadir_proxy_adflush/crawl_dir
mkdir /yopo-artifact/OpenWPM/datadir_proxy_adflush/log_dir
mkdir /yopo-artifact/OpenWPM/datadir_proxy_adflush/screenshots
mkdir /yopo-artifact/OpenWPM/datadir_proxy_adflush/sources
mkdir /yopo-artifact/scripts/perturb_html/running_check_adflush

monitor_path="/yopo-artifact/scripts/perturb_html/running_check_adflush"

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
    tmux new-session -d -s crawling_modification_adflush

    for i in {1..16}; do
        tmux new-window -t crawling_modification_adflush:$i
    done

    python3 /yopo-artifact/scripts/perturb_html/merge_mod_mappings_adflush.py --map-idx ${map_idx}

    command_proxy="cd /yopo-artifact/mitmproxy && . venv/bin/activate && mitmproxy --map-local-file /yopo-artifact/data/rendering_stream/mod_mappings_adflush/merged/merged_map_mod_${map_idx}.csv -p"
    echo "mapping command: $command_proxy"

    cd /yopo-artifact/mitmproxy

    tmux send-keys -t crawling_modification_adflush:1 "${command_proxy} 6866" Enter
    tmux send-keys -t crawling_modification_adflush:2 "${command_proxy} 6867" Enter
    tmux send-keys -t crawling_modification_adflush:3 "${command_proxy} 6868" Enter
    tmux send-keys -t crawling_modification_adflush:4 "${command_proxy} 6869" Enter
    tmux send-keys -t crawling_modification_adflush:5 "${command_proxy} 6870" Enter
    tmux send-keys -t crawling_modification_adflush:6 "${command_proxy} 6871" Enter
    tmux send-keys -t crawling_modification_adflush:7 "${command_proxy} 6872" Enter
    tmux send-keys -t crawling_modification_adflush:8 "${command_proxy} 6873" Enter
    tmux send-keys -t crawling_modification_adflush:9 "${command_proxy} 6874" Enter
    tmux send-keys -t crawling_modification_adflush:10 "${command_proxy} 6875" Enter
    tmux send-keys -t crawling_modification_adflush:11 "${command_proxy} 6876" Enter
    tmux send-keys -t crawling_modification_adflush:12 "${command_proxy} 6877" Enter
    tmux send-keys -t crawling_modification_adflush:13 "${command_proxy} 6878" Enter
    tmux send-keys -t crawling_modification_adflush:14 "${command_proxy} 6879" Enter
    tmux send-keys -t crawling_modification_adflush:15 "${command_proxy} 6880" Enter
    tmux send-keys -t crawling_modification_adflush:16 "${command_proxy} 6881" Enter

    tmux new-session -d -s crawling_modification_python_adflush
    for i in {1..16}; do
        tmux new-window -t crawling_modification_python_adflush:$i
    done

    command_python="conda deactivate && conda activate openwpm && python3 /yopo-artifact/OpenWPM/demo_proxy_auto_adflush.py --mapping-id ${map_idx} --crawler-id"
    echo "crawling command: $command_python"

    cd /yopo-artifact/mitmproxy

    sleep 5

    tmux send-keys -t crawling_modification_python_adflush:1 "${command_python} 0" Enter
    tmux send-keys -t crawling_modification_python_adflush:2 "${command_python} 1" Enter
    tmux send-keys -t crawling_modification_python_adflush:3 "${command_python} 2" Enter
    tmux send-keys -t crawling_modification_python_adflush:4 "${command_python} 3" Enter
    tmux send-keys -t crawling_modification_python_adflush:5 "${command_python} 4" Enter
    tmux send-keys -t crawling_modification_python_adflush:6 "${command_python} 5" Enter
    tmux send-keys -t crawling_modification_python_adflush:7 "${command_python} 6" Enter
    tmux send-keys -t crawling_modification_python_adflush:8 "${command_python} 7" Enter
    tmux send-keys -t crawling_modification_python_adflush:9 "${command_python} 8" Enter
    tmux send-keys -t crawling_modification_python_adflush:10 "${command_python} 9" Enter
    tmux send-keys -t crawling_modification_python_adflush:11 "${command_python} 10" Enter
    tmux send-keys -t crawling_modification_python_adflush:12 "${command_python} 11" Enter
    tmux send-keys -t crawling_modification_python_adflush:13 "${command_python} 12" Enter
    tmux send-keys -t crawling_modification_python_adflush:14 "${command_python} 13" Enter
    tmux send-keys -t crawling_modification_python_adflush:15 "${command_python} 14" Enter
    tmux send-keys -t crawling_modification_python_adflush:16 "${command_python} 15" Enter

    while true; do
        if check_files_exist; then
            break
        fi
        sleep 10
    done

    # Kill the existing sessions
    tmux kill-session -t crawling_modification_adflush
    tmux kill-session -t crawling_modification_python_adflush

    end_time=$(date +%s)
    total_time=$((end_time - start_time))
    
    echo "mapping $map_idx running time: $total_time seconds"
    sleep 10
done

echo "[Phase 2-4] Extract features for AdFlush..."
sleep 10
rm -rf /yopo-artifact/WebGraph/result_adflush
cd /yopo-artifact/WebGraph

source /opt/anaconda/etc/profile.d/conda.sh
conda activate openwpm
python code/run_automate_adflush.py

echo "[Phase 2-5] merge features for AdFlush..."
python3 code/my_utils_adflush.py

echo "[Phase 2-6] extract features for AdFlush..."
source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
python3 /yopo-artifact/scripts/crawler/adflush/filter_target_for_attack.py --attack-option ${attack_option}

echo "[Phase 2-7] running AdFlush feature extraction for AdFlush..."
source /opt/anaconda/etc/profile.d/conda.sh
conda activate adflush
cd /yopo-artifact/AdFlush/source
rm -rf /yopo-artifact/AdFlush/source/MY_jsfile
python3 /yopo-artifact/AdFlush/source/MY_embedding_automate.py --attack-option ${attack_option} > "$LOG_DIR/embedding_adflush.log"

echo "[Phase 2-8] re-preprocess for AdFlush..."
source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
python3 /yopo-artifact/scripts/crawler/adflush/preprocessing_RF_for_attack.py --attack-option ${attack_option}

echo "[Phase 2-9] Compute ASR for AdFlush..."
cd /yopo-artifact/scripts
test_UAP /yopo-artifact/data/dataset/ from_adflush/target_features_rf.csv modified_features_target_rf_decoded_drop_adflush_${attack_option}.csv /yopo-artifact/data/dataset/from_adflush/saved_model_adflush/rf_model_30perc.pt ${attack_option}
