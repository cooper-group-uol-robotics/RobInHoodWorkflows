###############################################################
# Prepares CC3 samples via TFB being added as a solid  # 
              
###############################################################

#Workflow for the CC3 synth workflow
#!/bin/bash

set -e

LOCAL_PATH=$(pwd)

DATASET_PATH="$LOCAL_PATH/data"


SAMPLES=(1 2 3) #vials to filter

FILTER_VOLUME=4 # Volume of the filter to be used in the workflow should be the sum of the volumes used in synthesis

CLEANING_VIAL=4 # Position of the vial used to clean the filtration funnel in the rack
CLEANING_SOLVENT="Ethanol" # Solvent used to clean the funnel before filtration

ANTI_SOLVENT="Ethanol" 
ANTI_SOLVENT_VOLUME=8

WASH_VOLUME=8 # Volume of the wash solvent to be used in the workflow
WASH_SOLVENT="95Ethanol_5DCM" # Solvent used to wash the solid after filtration
WASH_CYCLE=2 # Number of times the wash will be performed


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

echo "[INFO] Starting CC3 solid synth work-up workflow."
read_robot_state



for SAMPLE in "${SAMPLES[@]}"; do
    echo "[INFO] Filtering $SAMPLE" 
    python $LOCAL_PATH/src/CC3_synth_solid.py "filter_sample" $SAMPLE $FILTER_VOLUME $CLEANING_VIAL $CLEANING_SOLVENT $ANTI_SOLVENT $ANTI_SOLVENT_VOLUME $DATASET_PATH
    read_robot_state
    python $LOCAL_PATH/src/CC3_synth_solid.py "wash_filtered_sample" $SAMPLE $WASH_VOLUME $WASH_CYCLE $WASH_SOLVENT $DATASET_PATH
    read read_robot_state
    python $LOCAL_PATH/src/CC3_synth_solid.py "clean_filter_station" $CLEANING_SOLVENT $WASH_VOLUME $DATASET_PATH
    read_robot_state
done



echo "[INFO] All samples processed successfully."
echo "[INFO] Results saved in $DATASET_PATH"
echo "[INFO] Workflow completed successfully."
# End of CC3 synth workflow