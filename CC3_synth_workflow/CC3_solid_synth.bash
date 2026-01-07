###############################################################
# Prepares CC3 samples via TFB being added as a solid  # 
              
###############################################################

#Workflow for the CC3 synth workflow
#!/bin/bash

set -e

LOCAL_PATH=$(pwd)

DATASET_PATH="$LOCAL_PATH/data"


SAMPLES=(1 2 3)

ALDEHYDE_NAME="TFB"
ALDEHYDE_MASS=100

SOLVENT_NAME="DCM_TFA"
SOLVENT_VOL=2

AMINE_NAME="1S_2S_amine"
AMINE_VOL=2




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

echo "[INFO] Starting CC3 synth workflow."
read_robot_state

for SAMPLE in "${SAMPLES[@]}"; do
    echo "[INFO] Processing sample $SAMPLE"
    python $LOCAL_PATH/src/CC3_synth_solid.py "add_solid_aldehyde" $SAMPLE $DATASET_PATH $ALDEHYDE_NAME $ALDEHYDE_MASS
    read_robot_state
done

for SAMPLE in "${SAMPLES[@]}"; do
    echo "[INFO] Processing sample $SAMPLE"
    python $LOCAL_PATH/src/CC3_synth_solid.py "dispense_solvent" $SAMPLE $DATASET_PATH $SOLVENT_NAME $SOLVENT_VOL
    read_robot_state
done

for SAMPLE in "${SAMPLES[@]}"; do
    echo "[INFO] Processing sample $SAMPLE"
    python $LOCAL_PATH/src/CC3_synth_solid.py "add_amine_and_cap" $SAMPLE $DATASET_PATH $AMINE_NAME $AMINE_VOL
    read_robot_state
done

echo "[INFO] All samples processed successfully."
echo "[INFO] Results saved in $DATASET_PATH"
echo "[INFO] Workflow completed successfully."
# End of CC3 synth workflow