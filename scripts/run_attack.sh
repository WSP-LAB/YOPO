#!/bin/bash
set -e

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <epsilon> <cost_type> <target>"
    echo "Example: $0 10 DC adgraph"
    exit 1
fi

# 1) pick the epsilon value (5, 10, 20, 40)
epsilon="$1"

# 2) pick the cost type (DC, HCC, HSC, HJC)
cost_type="$2"

if [ "$cost_type" == "HJC" ]; then
    echo "Converting cost_type from HJC to HSC"
    cost_type="HSC"
fi

# 3) pick the target (adgraph, webgraph, adflush)
target="$3"


echo "===== Running attack with epsilon=${epsilon}, cost_type=${cost_type}, and target=${target} ====="

# Export the variables
export epsilon cost_type

case $target in
    "adgraph")
        ./attack_pipeline_adgraph.sh
        ;;
    "webgraph")
        ./attack_pipeline_webgraph.sh
        ;;
    "adflush")
        ./attack_pipeline_adflush.sh
        ;;
    "pagegraph")
        ./attack_pipeline_pagegraph.sh
        ;;
    *)
        echo "Unknown target: $target"
        exit 1
        ;;
esac
