#!/bin/bash
set -e

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <target>"
    echo "Example: $0 adflush"
    exit 1
fi

# 1) select the target (adgraph, webgraph, adflush, pagegraph)
target="$1"

echo "===== Crawling target AdBlocker :${target} ====="

case $target in
    "adgraph")
        ./run_crawler_adgraph.sh
        ;;
    "webgraph")
        ./run_crawler_webgraph.sh
        ;;
    "adflush")
        ./run_crawler_adflush.sh
        ;;
    "pagegraph")
        ./run_crawler_pagegraph.sh
        ;;
    *)
        echo "Unknown target: $target"
        exit 1
        ;;
esac

