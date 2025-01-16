#!/bin/bash
set -e

PYTHON_SCRIPT="/yopo-artifact/scripts/crawler/save_html_files.py"
NUM_CRAWLER=16
LOG_DIR="/yopo-artifact/logs"

# activate conda env
source /opt/anaconda/etc/profile.d/conda.sh
conda activate adgraph

# initialize html directory
echo "Now saving the HTML files... Check crawler.log files!"
rm -rf /yopo-artifact/data/rendering_stream/html
mkdir /yopo-artifact/data/rendering_stream/html

# Launch the Python script for each crawler
for i in $(seq 0 $((NUM_CRAWLER-1)))
do
    echo "Starting crawler $i..."
    python3 "$PYTHON_SCRIPT" --crawler-id "$i" --num-sites 10000 --num-crawler $NUM_CRAWLER > "$LOG_DIR/crawler_$i.log" 2>&1 &
done

wait

# Merge multiple mapping files into one
OUT_FNAME="/yopo-artifact/data/rendering_stream/tmp_final_url_to_html_filepath_mapping.csv"
rm -rf /yopo-artifact/data/rendering_stream/tmp_final_url_to_html_filepath_mapping.csv
rm -rf /yopo-artifact/data/rendering_stream/final_url_to_html_filepath_mapping.csv
rm -rf /yopo-artifact/data/rendering_stream/map_local_list_unmod_final.csv

sleep 3
cat /yopo-artifact/data/rendering_stream/final_url_to_html_filepath_mapping_*.csv > "$OUT_FNAME"
python3 -c "from utils import make_mapping_final; make_mapping_final()"

echo "Saving HTML files finished."
