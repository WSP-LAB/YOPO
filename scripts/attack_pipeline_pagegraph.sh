#!/bin/bash
set -e

generate_UAP() {
    python3 UAP_implement.py --csv-path $1 --csv-name-ad $2 --out-name $3 --delta-name $4 --model-fpath $5 --csv-target-name $6 --lagrangain $7 --sampling-size $8 --epsilon $9 --mode ${10} --cuda ${11}
}

test_UAP() {
    python3 test_ASR_pagegraph.py --csv-path $1 --csv-name-before-attack $2 --csv-name-final $3 --model-fpath $4 --attack-option $5
}

mode="pagegraph"
perc="30"
query_size="100000"
option="${perc}perc_${query_size}"
sampling_size="40000"
lagrangain="400"
attack_option="${perc}perc_inv${sampling_size}_query_${query_size}_lag_${lagrangain}_eps${epsilon}_${cost_type}_pagegraph"
map_count=$(ls /yopo-artifact/data/rendering_stream/mod_mappings_pagegraph/map_mod_* | wc -l)
LOG_DIR="/yopo-artifact/logs"
cuda="0"

echo "[Phase 2-1] generate a UAP for PageGraph..."
source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
generate_UAP /yopo-artifact/data/dataset/ final_${option}_for_inversion_pagegraph.csv perturbed_features_nbackdoor_${attack_option}.csv /delta_nbackdoor_${attack_option}.csv /yopo-artifact/data/dataset/from_pagegraph/saved_model_pagegraph/surrogate_${option}_weighted.pt from_pagegraph/target_features_rf.csv $lagrangain $sampling_size $epsilon $mode $cuda
conda deactivate

echo "[Phase 2-2] generate perturbed HTML for PageGraph..."
sleep 3
rm -rf /yopo-artifact/data/rendering_stream/modified_html_pagegraph
mkdir /yopo-artifact/data/rendering_stream/modified_html_pagegraph
rm -rf /yopo-artifact/data/rendering_stream/modified_features_pagegraph
mkdir /yopo-artifact/data/rendering_stream/modified_features_pagegraph
rm -rf /yopo-artifact/data/rendering_stream/modified_pagegraph
mkdir /yopo-artifact/data/rendering_stream/modified_pagegraph

source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph
cd /yopo-artifact/scripts/perturb_html
python3 /yopo-artifact/scripts/perturb_html/feature_map_back_pagegraph.py --attack-option ${attack_option} > "$LOG_DIR/perturb_html_pagegraph.log"

echo "[Phase 2-3] Building PageGraph..."
sleep 3
source /yopo-artifact/PageGraph/pagegraph-query/venv/bin/activate

cd /yopo-artifact/PageGraph/pagegraph-query
python rewrite_for_attack.py --mapping_path /yopo-artifact/data/rendering_stream/map_local_list_unmod_final.csv --html_path /yopo-artifact/data/rendering_stream/modified_html_pagegraph

cd /yopo-artifact/mitmproxy
if tmux list-sessions >/dev/null 2>&1; then
    echo "Killing tmux server..."
    tmux kill-server
else
    echo "No tmux server is running."
fi
./run_for_pagegraph.sh 32 /yopo-artifact/PageGraph/pagegraph-query/final_url_to_modified_html_filepath_mapping_AE_for_attack.csv

cd /yopo-artifact/PageGraph/pagegraph-crawl
python build_pagegraph.py --map-local-file /yopo-artifact/PageGraph/pagegraph-query/final_url_to_modified_html_filepath_mapping_AE_for_attack.csv -b /usr/bin/brave-browser -o /yopo-artifact/data/rendering_stream/modified_pagegraph -j 32 -t 600

echo "[Phase 2-4] Extracting features"
source /yopo-artifact/PageGraph/pagegraph-query/venv/bin/activate
cd /yopo-artifact/PageGraph/pagegraph-query
python extract_features.py --graph_dir /yopo-artifact/data/rendering_stream/modified_pagegraph --feature_dir /yopo-artifact/data/rendering_stream/modified_features_pagegraph --mapping_path /yopo-artifact/PageGraph/pagegraph-query/final_url_to_modified_html_filepath_mapping_AE_for_attack.csv -j 32 -t 600 --modified
deactivate

echo "[Phase 2-5] Merging csv"
cd /yopo-artifact/scripts/crawler
python3 -c "from utils import merging_mod_pagegraph; merging_mod_pagegraph()"

echo "[Phase 2-6] Extracting target features"
python3 /yopo-artifact/scripts/crawler/pagegraph/filter_target_for_attack.py --attack-option ${attack_option}

echo "[Phase 2-7] re-preprocess for PageGraph..."
python3 /yopo-artifact/scripts/crawler/pagegraph/preprocessing_RF_for_attack.py --attack-option ${attack_option}

echo "[Phase 2-8] compute ASR for PageGraph..."
cd /yopo-artifact/scripts
test_UAP /yopo-artifact/data/dataset/ from_pagegraph/target_features_rf.csv modified_features_target_rf_decoded_drop_${attack_option}.csv /yopo-artifact/data/dataset/from_pagegraph/saved_model_pagegraph/rf_model_30perc.pt ${attack_option}
