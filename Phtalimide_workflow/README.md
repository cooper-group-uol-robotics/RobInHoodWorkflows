<p align="center">
  <img src="https://raw.githubusercontent.com/FranciscoMunguiaGaleano/RobInHoodImgs/fb58da044365d0beac8132a96daffff3d9c79980/imgs/logo.png" alt="alt text" width="14%"></p>

# Phthalimide Synthesis Workflow

This directory contains an automated workflow for the synthesis and work-up of a functionalised phthalimide using the RobInHood robotic chemistry platform. The workflow is executed via a Bash script that coordinates sample preparation, heating and stirring, solvent addition, filtration, washing, and cleanup.

This workflow depends on the RobInHoodPy control framework and assumes a correctly configured RobInHood hardware setup.

## Overview

The workflow performs the following high-level steps:

### Sample preparation
Solid and liquid reagents are dispensed into multiple reaction vials using automated solid and liquid handling modules.

### Reflux reaction
Samples are heated to reflux temperature and stirred for an extended reaction period.

### Cooling and dilution
After the reaction, samples are cooled and diluted with water to aid downstream work-up.

### Filtration and washing
Reaction mixtures are filtered using a vacuum filtration module, followed by multiple wash cycles to improve product purity.

### System cleanup
The filtration system is rinsed between samples to prevent cross-contamination.

The entire process runs unattended once started, with intermediate note-taking and state checks to improve robotic reliability.

### Workflow Parameters

Key experimental parameters are defined at the top of the Bash script and can be easily modified:

1. Number of samples: defined via the SAMPLES array

2. Reaction temperature: 110 °C

3. Stirring speed: 400 rpm

4. Reaction time: 18 hours

5. Dilution solvent: Water

6. Wash solvent: Water (multiple wash cycles)

7. Filter cleaning solvent: Ethanol

This design allows the workflow to be adapted without modifying the underlying Python control logic.

### Running the Workflow

From within the Phtalimide_workflow directory:
```
bash synthesis.bash
```
The script will:

Create a data/ directory for logs and results (if it does not already exist)

Sequentially prepare and process each sample

Save run metadata and intermediate states for traceability

### Requirements

A fully configured RobInHood hardware platform

RobInHoodPy installed and accessible in the environment

Correctly populated reagent and configuration files required by RobInHoodPy

Core dependency:
👉 https://github.com/cooper-group-uol-robotics/RobInHoodPy.git

### Notes

Product recovery (e.g. drying and final isolation) is performed manually after the automated workflow completes.

Reaction yields and purity are validated offline using standard analytical techniques (e.g. NMR, MS).
