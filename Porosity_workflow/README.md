<p align="center">
  <img src="https://raw.githubusercontent.com/FranciscoMunguiaGaleano/RobInHoodImgs/fb58da044365d0beac8132a96daffff3d9c79980/imgs/logo.png" alt="alt text" width="14%"></p>
  
# Dye-Based Porosity Screening Workflow

This directory contains an automated workflow for dye-based porosity screening using the RobInHood robotic chemistry platform. The workflow prepares solid–dye samples, performs stirring, filtration, and imaging, and then passes the resulting data to the Colorimetry workflow for quantitative analysis.

The workflow is executed via a single Bash script (workflow.bash) and depends on the RobInHoodPy control framework.

## Overview

This workflow implements a qualitative porosity screening method based on dye uptake. A solid sample is exposed to multiple dyes of different molecular sizes. After stirring and filtration, colour loss in the dye solutions is analysed to infer material porosity.

The workflow consists of three main stages:

1. Sample preparation and mixing

2. Filtration and imaging

3. Colour analysis (via the [Colorimetry_workflow](https://github.com/cooper-group-uol-robotics/RobInHoodWorkflows/tree/ad86fb82fad053bc43498891f581f58269986caf/Colorimetry_workflow))

## Workflow Description

### Sample Preparation and Stirring

For each solid–dye pair, the workflow:

1. Prepares sample vials containing a solid material and a dye solution

2. Transfers the samples to a stirring hotplate

3. Stirs the mixtures for a defined period to allow dye uptake

4. Returns the samples to the vial rack

5. Multiple samples are handled sequentially, with robot state checks between actions to improve reliability.

### Filtration

After stirring, each sample is filtered using the RobInHood filtration module.
The filtration system is cleaned and conditioned between samples using a dedicated cleaning vial and solvent to prevent cross-contamination.

### Imaging

Following filtration, the filtered dye solutions are transferred to the vision module and photographed under controlled lighting conditions. Images and associated metadata are saved locally for downstream analysis.

## Colorimetry Analysis

The resulting images are analysed using the Colorimetry workflow located in the corresponding repository folder. This step quantifies colour intensity and dye concentration, enabling classification of samples as porous or non-porous.

ℹ️ The porosity workflow prepares and images the samples; colour analysis is performed by the separate Colorimetry_workflow.

## Running the Workflow

From within the Porosity_workflow directory:
```
bash workflow.bash
```

The script will:

- Create data/ and output directories if they do not exist

- Prepare, stir, filter, and image all samples

- Save images and metadata for colour analysis

### Output

Experimental logs and metadata are stored in data/

Image files and regions-of-interest (ROI) outputs are stored in data/ROI_output/

These outputs are consumed by the Colorimetry workflow for analysis

### Requirements

A fully configured RobInHood hardware platform

RobInHoodPy installed and available in the environment

The Colorimetry workflow available for downstream analysis

Core dependency:
👉 https://github.com/cooper-group-uol-robotics/RobInHoodPy.git

### Notes

The workflow is designed for high-throughput screening and can be extended to additional dyes or samples by modifying the script parameters.

Porosity classification is based on dye concentration thresholds defined during the colour analysis stage.
