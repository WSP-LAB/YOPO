#!/bin/bash
set -e

generate_query() {
    echo "[PHASE 1-1] Generating queries for WebGraph..."
    python3 generate_query.py --csv-path $1 --csv-name $2 --nn-csv-name $3 --model-fpath $4 --perc $5 --query-size $6 --mode $7
}

train_surrogate() {
    echo "[PHASE 1-2] Training surrogate model for WebGraph..."
    python3 surrogate_cross.py --csv-path $1 --csv-name $2 --save-fpath $3 --mode $4
}


perc="30"
query_size="100000"
option="${perc}perc_${query_size}"
sampling_size="40000"
epsilon="10"
lagrangain="400"
attack_option="${perc}perc_inv${sampling_size}_query_${query_size}_lag_${lagrangain}_eps${epsilon}"
mode="webgraph"
cuda="0"

source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph

generate_query /yopo-artifact/data/dataset/from_webgraph/ features_rf.csv features_nn.csv saved_model_webgraph/rf_model_${perc}perc.pt ${perc} ${query_size} webgraph

train_surrogate /yopo-artifact/data/dataset/for_surrogate/ final_query_${option}_webgraph.csv /yopo-artifact/data/dataset/from_webgraph/saved_model_webgraph/surrogate_${option}_weighted.pt webgraph

conda deactivate