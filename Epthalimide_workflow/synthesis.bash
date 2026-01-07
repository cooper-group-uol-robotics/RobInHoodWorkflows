
#Workflow for Ram project
#!/bin/bash
set -e


LOCAL_PATH=$(pwd)
DATA_PATH="$LOCAL_PATH/data" 

#These correspond to the samples in the setup file
SAMPLES=(0 1 2)

#Temperature for the reaction
TEMPERATURE=110

#Stirring speed for the reaction
SPEED=400

#Time for the reaction
SECS=0
MINS=0
HOURS=18

#Position of the vial used to clean the filter before filtering the samples
CLEANING_VIAL=14
CLEANING_SOLVENT="Water(DI)"
CLEANING_SOLVENT_VOL=8 #ml

#Solvent name and volume to add to the samples for washing/dilution
SOLVENT="Water(DI)"
DILUTE_SOLVENT_VOLUME=6 #ml
WASH_SOLVENT_VOLUME=10
WASH_CYCLES=2


#Position of the filter used to clean the samples
FILT_CLEANING_SOLVENT="Ethanol"
FILT_CLEANING_SOLVENT_VOL=10 #ml



read_robot_state(){
    python $LOCAL_PATH/src/read_current_state.py
    python $LOCAL_PATH/src/read_current_state.py
    python $LOCAL_PATH/src/read_current_state.py
}


if [ ! -d "$DATA_PATH" ]; then
    echo "[WARNING] Directory $DATA_PATH does not exist."
    mkdir -p "$DATA_PATH"
    echo "[WARNING] Directory $DATA_PATH has been created."
else 
    echo "[INFO] Directory $DATA_PATH already exists."
fi



echo "[INFO] Script running in $LOCAL_PATH"
echo "[INFO] Results will be saved in $DATA_PATH"

echo "[INFO] Reading robot state:"
read_robot_state 


echo "[INFO] Step 1: Preparing samples."


for sample in "${SAMPLES[@]}"; do
    echo "[INFO] Preparing sample $sample"
    read_robot_state
    python $LOCAL_PATH/src/synthesis.py "prepare_samples" $sample $DATA_PATH
done

echo "[INFO] Reading robot state:"
read_robot_state

echo "[INFO] Step 3: Stirring and heating samples."

echo "[INFO] Setting hotplate to heat" 

python $LOCAL_PATH/src/synthesis.py "heat_stirr" $TEMPERATURE $SPEED $DATA_PATH 


echo "[INFO] Moving samples to the hotplate"

for sample in "${SAMPLES[@]}"; do
   echo "[INFO] Moving sample $sample to the hotplate"
   read_robot_state
   python $LOCAL_PATH/src/synthesis.py "samples_to_hotplate" $sample $DATA_PATH
done


echo "[INFO] Reading robot state:"
read_robot_state


echo "[INFO] Starting the reaction timer"

python $LOCAL_PATH/src/synthesis.py "reaction_timer" $DATA_PATH $HOURS $MINS $SECS


echo "[INFO] Step 4: Moving samples to the rack."

for i in "${!SAMPLES[@]}"; do
   echo "[INFO] Moving sample ${SAMPLES[-1 - $i]} to the rack"
   read_robot_state
   python $LOCAL_PATH/src/synthesis.py "store_samples" ${SAMPLES[-1 - $i]} $DATA_PATH 
done

echo "[INFO] Reading robot state:"
read_robot_state

echo "[INFO] Step 5: Adding water to samples"

for sample in "${SAMPLES[@]}"; do
    echo "[INFO] Adding water to sample $sample"
    read_robot_state
    python $LOCAL_PATH/src/synthesis.py "add_solvent" $sample $SOLVENT $DILUTE_SOLVENT_VOLUME $DATA_PATH
done

echo "[INFO] waiting for sample to cool to near room temperature"
python $LOCAL_PATH/src/synthesis.py "heat_stirr" 30 $SPEED $DATA_PATH


for sample in "${SAMPLES[@]}"; do
    echo "[INFO] Moving samples to hotplate $sample"
    read_robot_state
    python $LOCAL_PATH/src/synthesis.py "samples_to_hotplate" $sample $DATA_PATH 
done

echo "[INFO] Stirring samples on hotplate"

python $LOCAL_PATH/src/synthesis.py "heat_stirr" 30 $SPEED $DATA_PATH
python $LOCAL_PATH/src/synthesis.py "reaction_timer" $DATA_PATH 0 20 0

for i in "${!SAMPLES[@]}"; do
   echo "[INFO] Moving sample ${SAMPLES[-1 - $i]} to the rack"
   read_robot_state
   python $LOCAL_PATH/src/synthesis.py "store_samples" ${SAMPLES[-1 - $i]} $DATA_PATH 
done

echo "[INFO] Step 5: Filtering samples"

for sample in "${SAMPLES[@]}"; do
    echo "[INFO] Filtering sample $sample"
    read_robot_state
    python $LOCAL_PATH/src/synthesis.py "filter_samples" "$sample" $CLEANING_VIAL $CLEANING_SOLVENT $DATA_PATH
    python $LOCAL_PATH/src/synthesis.py "wash_filtered_sample" $sample $WASH_SOLVENT_VOLUME $WASH_CYCLES $SOLVENT $DATA_PATH
    python $LOCAL_PATH/src/synthesis.py "clean_filter" $FILT_CLEANING_SOLVENT $FILT_CLEANING_SOLVENT_VOL $DATA_PATH
done

echo "[INFO] Worklfow complete"