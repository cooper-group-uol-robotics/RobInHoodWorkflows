#!/bin/bash
set -e

LOCAL_PATH=$(pwd)
TEMP_PATH="$LOCAL_PATH/dataset"
DATASET_PATH="$TEMP_PATH/$1/imgs"
OUTPUT_PATH="$TEMP_PATH/$1/ROI_output"


if [ ! -d "$DATASET_PATH" ]; then
    echo "[WARNING] Directory $DATASET_PATH does not exist."
    mkdir -p "$DATASET_PATH"
    mkdir -p "$OUTPUT_PATH"
    echo "[WARNING] Directory $DATASET_PATH has been created."
else 
    echo "[INFO] Directory $DATASET_PATH already exists."
fi

if [ ! -d "$OUTPUT_PATH" ]; then
    echo "[WARNING] Directory $OUTPUT_PATH does not exist."
    mkdir -p "$OUTPUT_PATH"
    echo "[WARNING] Directory $OUTPUT_PATH has been created."
else 
    echo "[INFO] Directory $OUTPUT_PATH already exists."
fi

echo "[INFO] Colorimetry"
python $LOCAL_PATH/colorimetry.py $1 $LOCAL_PATH"/" 