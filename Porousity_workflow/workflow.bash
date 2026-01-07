###############################################################
# Prepares 6 samples of a given solid and one different dye   # 
# each [dye1, dye2, dye3, dye4, dye5, dye6]                   #
###############################################################

#Workflow for the Dye Porosity screen
#!/bin/bash

#set -e

LOCAL_PATH=$(pwd)

DATASET_PATH="$LOCAL_PATH/data"
OUTPUT_PATH="$LOCAL_PATH/data/ROI_output"

SAMPLE_PAIRS=("0 7" "1 8")

SPEED=200
SECS=30
MINS=0
HOURS=0

CLEANING_VIAL=13
CLEANING_SOLVENT="Water(DI)"

#reverse the order of the samples for removing them from the hotplate
REVERSE=()
LENGTH=${#SAMPLE_PAIRS[@]}
for (( i=$LENGTH-1; i>=0; i-- )); do
        REVERSE+=("${SAMPLE_PAIRS[i]}")
done


read_robot_state(){
    python $LOCAL_PATH/src/read_current_state.py
    python $LOCAL_PATH/src/read_current_state.py
    python $LOCAL_PATH/src/read_current_state.py
}

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

echo "[INFO] Script running in $LOCAL_PATH"
echo "[INFO] Results will be saved in $DATASET_PATH"

echo "[INFO] Reading robot state:"
read_robot_state 


echo "[INFO] Preparing samples in progress."

for pair in "${SAMPLE_PAIRS[@]}"; do
    read_robot_state
    readarray -d ' ' sample <<< "$pair"
    echo "[INFO] Preparing sample ${sample[0]}"
    python $LOCAL_PATH/src/dye_workflow.py "prepare_sample" $sample[0] $DATASET_PATH
    
done

echo "[INFO] Reading robot state:"
read_robot_state


# for pair in "${SAMPLE_PAIRS[@]}"; do
#     read_robot_state
#     readarray -d ' ' sample <<< "$pair"
#     echo "[INFO] Preparing sample ${sample[0]}"
#     python $LOCAL_PATH/src/dye_workflow.py "sample_rack_to_ika" $sample[0] $DATASET_PATH
    
# done

# echo "[INFO] Reading robot state:"
# read_robot_state

# echo "[INFO] Step 3: Stirring samples."
# python $LOCAL_PATH/src/dye_workflow.py "stirr_samples" $DATASET_PATH $SPEED $SECS $MINS $HOURS

# echo "[INFO] Reading robot state:"
# read_robot_state

# echo "[INFO] Moving samples to rack."
    
# for pair in "${REVERSE[@]}"; do
#     read_robot_state
#     readarray -d ' ' sample <<< "$pair"
#     echo "[INFO] Moving sample ${sample[0]} to the rack"
#     python $LOCAL_PATH/src/dye_workflow.py "store_sample" $sample[0] $DATASET_PATH
# done


# echo "[INFO] Filtering samples"
# for pair in "${SAMPLE_PAIRS[@]}"; do
#     echo "[INFO] Reading robot state:"
#     read_robot_state
#     python $LOCAL_PATH/src/dye_workflow.py "filter_sample" $DATASET_PATH $pair $CLEANING_VIAL $CLEANING_SOLVENT
# done

echo "[INFO] Reading robot state:"
read_robot_state

echo "[INFO] Photographing samples"
for pair in "${SAMPLE_PAIRS[@]}"; do
    read_robot_state
    python $LOCAL_PATH/src/dye_workflow.py "photograph_sample" $pair $DATASET_PATH
    
done

echo "[INFO] Colorimetry"
#colorimetry tbd

echo "[INFO] Reading robot state:"
read_robot_state



echo "[INFO] Process complete."