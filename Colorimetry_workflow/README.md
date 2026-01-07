<p align="center">
  <img src="https://raw.githubusercontent.com/FranciscoMunguiaGaleano/RobInHoodImgs/fb58da044365d0beac8132a96daffff3d9c79980/imgs/logo.png" alt="alt text" width="14%"></p>

# Colorimetry Workflow

This workflow performs image-based colorimetry to estimate dye concentrations from samples prepared and imaged by the Porosity workflow.

It converts pixel intensities from predefined Regions of Interest (ROIs) into dye concentration values (ppm) using pre-calibrated models.

## Overview

The colorimetry is performed as follows: 

1. Loads sample images produced by the Porosity workflow

2. Extracts a fixed ROI from each image

3. Computes mean pixel values within the ROI

4. Converts pixel values to dye concentration (ppm) using dye-specific calibration curves

5. Saves processed results to disk

### Calibration 

Calibration is based on reference samples at 1, 2, 4, 6, 8, and 10 ppm

Each dye uses a specific colour channel (RGB / HSV / LAB / grayscale) chosen for robustness

Calibration curves are pre-fitted and inverted to predict ppm from pixel intensity

Accuracy is highest near 1 ppm, which is the decision threshold used in porosity screening

### Running the workflow
```
bash colorimetry.bash <sample_name>
```

<sample_name> must match the dataset folder created by the Porosity workflow.

### Folder structure
```
dataset/
└── <sample_name>/
    ├── imgs/         # Input images
    └── ROI_output/   # Colorimetry results
````

### Output

Mean ROI pixel values

Estimated dye concentration (ppm)

Per-sample colorimetry results stored in ROI_output/

### Notes

Designed to be reproducible across different cameras and lightboxes

Saturation effects may occur near 0 and 10 ppm

Measurements near 1 ppm are reliable and used for automated decision-making
