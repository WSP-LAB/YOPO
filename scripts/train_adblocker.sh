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

# Export the variables
export epsilon cost_type

case $target in
    "adgraph")
        ./train_random_forest_adgraph.sh
        ;;
    "webgraph")
        ./train_random_forest_webgraph.sh
        ;;
    "adflush")
        ./train_random_forest_adflush.sh
        ;;
    "pagegraph")
        ./train_random_forest_pagegraph.sh
        ;;
    *)
        echo "Unknown target: $target"
        exit 1
        ;;
esac
