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
        ./crawl_adgraph.sh
        ;;
    "webgraph")
        ./crawl_webgraph.sh
        ;;
    "adflush")
        ./crawl_adflush.sh
        ;;
    "pagegraph")
        ./crawl_pagegraph.sh
        ;;
    *)
        echo "Unknown target: $target"
        exit 1
        ;;
esac

