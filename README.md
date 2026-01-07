<p align="center">
  <img src="https://raw.githubusercontent.com/FranciscoMunguiaGaleano/RobInHoodImgs/fb58da044365d0beac8132a96daffff3d9c79980/imgs/logo.png" alt="alt text" width="14%"></p>

# Workflows

This repository contains example experimental workflows developed for the RobInHood robotic chemistry platform. Each workflow demonstrates an end-to-end automated experiment executed inside a standard laboratory fume hood.

All workflows in this repository depend on the core RobInHood control software.

### Dependency

This repository requires RobInHoodPy to be installed and correctly configured:

👉 https://github.com/cooper-group-uol-robotics/RobInHoodPy.git

The workflows here assume:

A functioning RobInHood hardware setup

Device drivers and configuration files provided by RobInHoodPy

Correctly populated reagent and sample configuration files

Repository Structure

Each workflow is contained in its own directory and is executed via a dedicated .bash script.

```text
├── CC3_synth_workflow/
│   └── CC3_solid_synth.bash
│   └── CC3_solid_workup.bash
├── Colorimetry_workflow/
│   └── colorimetry.bash
├── Porosity_workflow/
│   └── workflow.bash
├── Phtalimide_workflow/
│   └── synthesis.bash
```

The .bash scripts launch Python-based workflows implemented using the RobInHoodPy API.

## Included Workflows

### Dye-Based Porosity Screening

(Porosity_workflow. Colorimetry_workflow)

Automated high-throughput porosity screening based on dye uptake and colour analysis. Samples are prepared, mixed with dye solutions, filtered, and analysed using computer vision. Porosity is inferred from colour loss across multiple dyes with different molecular sizes.

This workflow runs fully autonomously from sample preparation to imaging and supports screening of materials such as CMPs, porous organic cages, and MOFs.

### CC3 Cage Synthesis

(CC3_synth_workflow)

Automated synthesis and work-up of the porous organic cage CC3. The workflow includes solid and liquid dispensing, long reaction times, antisolvent addition, repeated washing, and filtration.

This case study demonstrates RobInHood’s ability to handle low-solubility reagents, multistep purification, and extended unattended operation.

### Phthalimide Synthesis

(Phtalimide_workflow)

Automated synthesis of a functionalised phthalimide via reflux, followed by aqueous work-up and filtration. The workflow includes heating, stirring, decapping, washing, and solid isolation.

This example highlights RobInHood’s suitability for multistep organic synthesis workflows involving heating and solid recovery.

### Running a Workflow

Each workflow is started by executing its corresponding .bash script.
Experimental parameters such as reagent identities, quantities, and vial positions are defined through configuration files and variables consumed by RobInHoodPy, allowing workflows to be adapted without modifying core control logic.
