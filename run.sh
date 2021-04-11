#!/bin/bash

if [ $# -eq 0 ]; then
    echo "./run <folder> <arguments>"
    exit
fi

folder=$1
args="${*:2}"
echo $args
rm -rf "$folder"
python optimize.py --save "$folder" $args
python export_results.py --folder "$folder" --export-pseudo-weights
python decision_making.py --folder "$folder"
./montage.sh "$folder"