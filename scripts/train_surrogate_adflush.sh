#!/bin/bash
set -e

generate_query() {
    echo "[PHASE 1-1] Generating queries for AdFlush..."
    python3 generate_query.py --csv-path $1 --csv-name $2 --nn-csv-name $3 --model-fpath $4 --perc $5 --query-size $6 --mode $7
    }

train_surrogate() {
    echo "[PHASE 1-2] Training surrogate model for AdFlush..."
    python3 surrogate_cross.py --csv-path $1 --csv-name $2 --save-fpath $3 --mode $4
    }


perc="30"
query_size="100000"
option="${perc}perc_${query_size}"
sampling_size="40000"
epsilon="10"
lagrangain="400"
attack_option="${perc}perc_inv${sampling_size}_query_${query_size}_lag_${lagrangain}_eps${epsilon}"
mode="adflush"
cuda="1"

source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph

generate_query /yopo-artifact/data/dataset/from_adflush/ features_rf.csv features_nn.csv saved_model_adflush/rf_model_${perc}perc.pt ${perc} ${query_size} adflush

train_surrogate /yopo-artifact/data/dataset/for_surrogate/ final_query_${option}_adflush.csv /yopo-artifact/data/dataset/from_adflush/saved_model_adflush/surrogate_${option}_weighted.pt adflush

conda deactivate