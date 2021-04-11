#!/bin/sh

if [ $# -ne 1 ]; then
    echo "./montage.sh <folder>"
    exit
fi

find "$1"/* -maxdepth 1 -type d -exec montage -density 300 -tile 2x0 -geometry +0+0 -border 1 "{}/*.png" {}/out.png \;
