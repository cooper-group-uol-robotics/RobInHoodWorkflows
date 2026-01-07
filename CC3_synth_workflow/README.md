<p align="center">
  <img src="https://raw.githubusercontent.com/FranciscoMunguiaGaleano/RobInHoodImgs/fb58da044365d0beac8132a96daffff3d9c79980/imgs/logo.png" alt="alt text" width="14%"></p>
  
# CC3 Cage Synthesis Workflow

This directory contains an automated workflow for the synthesis and work-up of the porous organic cage CC3 using the RobInHood robotic chemistry platform. The workflow is divided into two sequential Bash scripts, covering reaction setup and post-reaction work-up.

Both scripts rely on the RobInHoodPy control framework and assume a fully configured RobInHood hardware system.

## Overview

The CC3 workflow is split into two stages:

Synthesis — automated preparation of CC3 reaction mixtures

Work-up — automated antisolvent addition, filtration, and washing

This separation allows long reaction times to be handled independently from downstream processing.

## Script 1: CC3 Solid Synthesis

(CC3_solid_synth.bash)

This script prepares CC3 samples by dispensing solid and liquid reagents into reaction vials and initiating the cage-forming reaction.

### Performed steps

1. Dispensing solid benzene-1,3,5-tricarboxaldehyde (TFB) into sample vials

2. Addition of solvent containing catalyst

3. Addition of diamine solution

4. Automated capping of reaction vials

5. Multiple samples can be prepared in parallel by modifying the SAMPLES array at the top of the script.

## Script 2: CC3 Solid Work-Up

(CC3_solid_workup.bash)

This script performs the automated isolation and washing of the CC3 product following the reaction period.

### Performed steps

1. Conditioning and cleaning of the filtration system

2. Antisolvent addition to precipitate CC3

3. Vacuum filtration of reaction mixtures

4. Repeated washing of the solid product

5. Cleaning of the filtration station between samples

The product is left to dry on the filter and is recovered manually after the workflow completes.

### Workflow Parameters

Key experimental parameters (e.g. sample positions, reagent masses, solvent volumes, wash cycles) are defined at the top of each Bash script and can be adjusted without modifying the underlying Python code.

### Running the Workflow

Run the scripts sequentially from the CC3_synth_workflow directory:

```
bash CC3_solid_synth.bash

# Allow the reaction to proceed for the desired time 

bash CC3_solid_workup.bash
```

All logs and intermediate data are stored in the local data/ directory.

### Requirements

A fully configured RobInHood hardware platform

RobInHoodPy installed and accessible in the environment

Core dependency:
👉 https://github.com/cooper-group-uol-robotics/RobInHoodPy.git

### Notes

Reaction times between synthesis and work-up are user-defined and may span multiple days.

Final drying and solid recovery are performed manually.

Product identity and phase purity are confirmed offline using standard analytical techniques.
