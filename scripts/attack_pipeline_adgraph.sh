#!/bin/bash
set -e

generate_UAP() {
    python3 UAP_implement.py --csv-path $1 --csv-name-ad $2 --out-name $3 --delta-name $4 --model-fpath $5 --csv-target-name $6 --lagrangain $7 --sampling-size $8 --epsilon $9 --mode ${10} --cuda ${11}
}

test_UAP() {
    python3 test_ASR_adgraph.py --csv-path $1 --csv-name-before-attack $2 --csv-name-final $3 --model-fpath $4 --attack-option $5
}

mode="adgraph"
perc="30"
query_size="100000"
option="${perc}perc_${query_size}"
sampling_size="40000"
lagrangain="400"
attack_option="${perc}perc_inv${sampling_size}_query_${query_size}_lag_${lagrangain}_eps${epsilon}_${cost_type}_adgraph"
map_count=$(ls /yopo-artifact/data/rendering_stream/mod_mappings_adgraph/map_mod_* | wc -l)
LOG_DIR="/yopo-artifact/logs"
cuda="0"


echo "[Phase 2-1] generate a UAP for AdGraph..."
source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
generate_UAP /yopo-artifact/data/dataset/ final_${option}_for_inversion_adgraph.csv perturbed_features_nbackdoor_${attack_option}.csv /delta_nbackdoor_${attack_option}.csv /yopo-artifact/data/dataset/from_adgraph/saved_model_adgraph/surrogate_${option}_weighted.pt from_adgraph/target_features_rf.csv $lagrangain $sampling_size $epsilon $mode $cuda
conda deactivate

echo "[Phase 2-2] generate perturbed HTML for AdGraph..."
sleep 5
rm -rf /yopo-artifact/data/rendering_stream/modified_html_adgraph
mkdir /yopo-artifact/data/rendering_stream/modified_html_adgraph

source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
cd /yopo-artifact/scripts/perturb_html
python3 /yopo-artifact/scripts/perturb_html/feature_map_back_adgraph.py --attack-option ${attack_option} > "$LOG_DIR/perturb_html_adgraph.log"

echo "[Phase 2-3] Crawling modified websites for AdGraph... Total map_count: $map_count"
rm -rf /root/rendering_stream
rm -rf /yopo-artifact/scripts/perturb_html/running_check_adgraph
mkdir /yopo-artifact/scripts/perturb_html/running_check_adgraph

monitor_path="/yopo-artifact/scripts/perturb_html/running_check_adgraph"

function check_files_exist() {
    for i in {1..10}; do
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
    for i in {1..10}; do
        rm -rf "${monitor_path}/End_${i}"
    done
    sleep 3
    
    # Create new session
    tmux new-session -d -s crawling_modification

    for i in {1..10}; do
        tmux new-window -t crawling_modification:$i
    done

    command_proxy="cd /yopo-artifact/mitmproxy && . venv/bin/activate && mitmproxy --map-local-file /yopo-artifact/data/rendering_stream/mod_mappings_adgraph/map_mod_${map_idx}.csv -p"
    echo "mapping command: $command_proxy"

    cd /yopo-artifact/mitmproxy

    tmux send-keys -t crawling_modification:1 "${command_proxy} 6666" Enter
    tmux send-keys -t crawling_modification:2 "${command_proxy} 6667" Enter
    tmux send-keys -t crawling_modification:3 "${command_proxy} 6668" Enter
    tmux send-keys -t crawling_modification:4 "${command_proxy} 6669" Enter
    tmux send-keys -t crawling_modification:5 "${command_proxy} 6670" Enter
    tmux send-keys -t crawling_modification:6 "${command_proxy} 6671" Enter
    tmux send-keys -t crawling_modification:7 "${command_proxy} 6672" Enter
    tmux send-keys -t crawling_modification:8 "${command_proxy} 6673" Enter
    tmux send-keys -t crawling_modification:9 "${command_proxy} 6674" Enter
    tmux send-keys -t crawling_modification:10 "${command_proxy} 6675" Enter

    # tmux attach-session -t crawling_modification

    tmux new-session -d -s crawling_modification_python
    for i in {1..10}; do
        tmux new-window -t crawling_modification_python:$i
    done

    command_python="conda deactivate && conda activate adgraph && python3 /yopo-artifact/scripts/perturb_html/test_adgraph.py --mapping-id ${map_idx} --crawler-id"
    echo "crawling command: $command_python"

    cd /yopo-artifact/mitmproxy

    sleep 10

    tmux send-keys -t crawling_modification_python:1 "${command_python} 0" Enter
    tmux send-keys -t crawling_modification_python:2 "${command_python} 1" Enter
    tmux send-keys -t crawling_modification_python:3 "${command_python} 2" Enter
    tmux send-keys -t crawling_modification_python:4 "${command_python} 3" Enter
    tmux send-keys -t crawling_modification_python:5 "${command_python} 4" Enter
    tmux send-keys -t crawling_modification_python:6 "${command_python} 5" Enter
    tmux send-keys -t crawling_modification_python:7 "${command_python} 6" Enter
    tmux send-keys -t crawling_modification_python:8 "${command_python} 7" Enter
    tmux send-keys -t crawling_modification_python:9 "${command_python} 8" Enter
    tmux send-keys -t crawling_modification_python:10 "${command_python} 9" Enter

    while true; do
        if check_files_exist; then
            break
        fi
        sleep 10
    done

    # Kill the existing sessions
    tmux kill-session -t crawling_modification
    tmux kill-session -t crawling_modification_python

    end_time=$(date +%s)
    total_time=$((end_time - start_time))
    
    echo "mapping $map_idx running time: $total_time seconds"
    sleep 10
done

echo "[Phase 2-4] parsing for AdGraph..."
sleep 5
mv /root/rendering_stream /root/modified_timeline
rm -rf /yopo-artifact/data/rendering_stream/modified_timeline
mv /root/modified_timeline /yopo-artifact/data/rendering_stream/modified_timeline
sleep 5

source /opt/anaconda/etc/profile.d/conda.sh
conda activate python2
python /yopo-artifact/scripts/crawler/adgraph/rules_parsing_for_attack.py

echo "[Phase 2-5] extract features for AdGraph..."
rm -rf /yopo-artifact/data/rendering_stream/modified_features
rm -rf /yopo-artifact/data/rendering_stream/modified_mappings
mkdir /yopo-artifact/data/rendering_stream/modified_features
mkdir /yopo-artifact/data/rendering_stream/modified_mappings
source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
python3 /yopo-artifact/scripts/crawler/adgraph/extract_features_for_attack.py --attack-option ${attack_option}

echo "[Phase 2-6] merge features for AdGraph..."
source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
python3 /yopo-artifact/scripts/crawler/adgraph/merge_features_for_attack.py

echo "[Phase 2-7] extract features for AdGraph..."
source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
python3 /yopo-artifact/scripts/crawler/adgraph/filter_target_for_attack.py --attack-option ${attack_option}

echo "[Phase 2-8] re-preprocess for AdGraph..."
source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
python3 /yopo-artifact/scripts/crawler/adgraph/preprocessing_RF_for_attack.py --attack-option ${attack_option}

echo "[Phase 2-9] compute ASR for AdGraph..."
cd /yopo-artifact/scripts
test_UAP /yopo-artifact/data/dataset/ from_adgraph/target_features_rf.csv modified_features_target_rf_decoded_drop_${attack_option}.csv /yopo-artifact/data/dataset/from_adgraph/saved_model_adgraph/rf_model_30perc.pt ${attack_option}
