###############################################################
# Prepares 6 samples of a given solid and one different dye   # 
# each [dye1, dye2, dye3, dye4, dye5, dye6]                   #
###############################################################

#!/bin/bash

LOCAL_PATH=$(pwd)
TEMP_PATH="$LOCAL_PATH/TEMP"
DATASET_PATH="$TEMP_PATH/$1/imgs/"
LOGNAME="$2"


SAMPLE_PAIRS=("1 7" "2 8" "3 9" "4 10" "5 11" "6 12")

read_robot_state(){
    python $LOCAL_PATH/src/read_current_state.py
    python $LOCAL_PATH/src/read_current_state.py
    python $LOCAL_PATH/src/read_current_state.py
}

if [ ! -d "$DATASET_PATH" ]; then
    echo "[WARNING] Directory $DATASET_PATH does not exist."
    mkdir -p "$DATASET_PATH"
    echo "[WARNING] Directory $DATASET_PATH has been created."
else 
    echo "[INFO] Directory $DATASET_PATH already exists."
fi

echo "[INFO] Script running in $LOCAL_PATH"
echo "[INFO] Results will be saved in $DATASET_PATH"
echo "[INFO] Reading robot state:"

#read_robot_state 
#echo "[INFO] Priming pump lines."
#python $LOCAL_PATH/main.py "prime_lines"

#echo "[INFO] Reading robot state:"
#read_robot_state 

# echo "[INFO] Preparing samples in progress."
# python $LOCAL_PATH/main.py "prepare_samples"

# echo "[INFO] Reading robot state:"
# read_robot_state

# echo "[INFO] Storing Samples"
# python $LOCAL_PATH/main.py "store_samples"


#read_robot_state

# echo "[INFO] Photograph post-dispense"
# python $LOCAL_PATH/main.py "photograph_samples_postprep" $1 $DATASET_PATH

# echo "[INFO] Moving to IKA"
# python $LOCAL_PATH/main.py "samples_rack_to_ika"

# echo "[INFO] Reading robot state:"
# read_robot_state

# echo "[INFO] Step 3: Stirring samples."
# python $LOCAL_PATH/main.py "stirr_samples"

# echo "[INFO] Reading robot state:"
# read_robot_state

# echo "[INFO] Moving samples to rack."
# python $LOCAL_PATH/main.py "store_samples"

# echo "[INFO] Photograph post stir"
# python $LOCAL_PATH/main.py "photograph_samples_poststir" $1 $DATASET_PATH

echo "[INFO] Reading robot state:"
read_robot_state

echo "[INFO] Filtering samples"
for pair in "${SAMPLE_PAIRS[@]}"; do
    python $LOCAL_PATH/main.py "filter_samples" $pair
done

echo "[INFO] Reading robot state:"
read_robot_state

echo "[INFO] Photographing samples post filter"
python $LOCAL_PATH/main.py "photograph_samples" $1 $DATASET_PATH

echo "[INFO] Process complete."
