#!/bin/bash
set -e

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <target>"
    echo "Example: $0 adgraph"
    exit 1
fi

# 1) select the target (adgraph, webgraph, adflush, pagegraph)
target="$1"

echo "===== Training target AdBlocker :${target} ====="

# Activate conda env
source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph

case $target in
    "adgraph")
        python3 train_random_forest_adgraph.py
        ;;
    "webgraph")
        python3 train_random_forest_webgraph.py
        ;;
    "adflush")
        python3 train_random_forest_adflush.py
        ;;
    "pagegraph")
        python3 train_random_forest_pagegraph.py
        ;;
    *)
        echo "Unknown target: $target"
        exit 1
        ;;
esac
