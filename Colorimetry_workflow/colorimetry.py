# -*- coding: utf-8 -*-
"""
Colorimetry-based porosity analysis

@author: Francisco
"""

import sys
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.stats import linregress
from scipy.optimize import curve_fit
from scipy import stats

# Constants
SQUARE_SIZE = 50
X_OFFSET = 10
Y_OFFSET = 45
CHANNELS = ["A", "B", "S", "L", "gray", "B"]
BARNEY_PARAMETERS = [[] for _ in range(6)]

# ---------------------- IMAGE PROCESSING ---------------------- #
def draw_center_square(image_path, output_path, square_size=SQUARE_SIZE, channel='B'):
    """Draw a square in the center of an image and return the median pixel value of the selected channel."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    B, G, R = cv2.split(image)
    H, S, V = cv2.split(hsv)
    L, A, BB = cv2.split(lab)

    channels = {
        'gray': gray, 'B': B, 'G': G, 'R': R,
        'H': H, 'S': S, 'V': V, 'L': L, 'A': A, 'BB': BB
    }

    height, width = gray.shape
    cx, cy = width // 2 + X_OFFSET, height // 2 + Y_OFFSET
    x1, y1 = cx - square_size // 2, cy - square_size // 2
    x2, y2 = cx + square_size // 2, cy + square_size // 2

    square = channels[channel][y1:y2, x1:x2]
    median_value = np.median(square)

    # Draw rectangle and save image
    img_copy = channels[channel].copy() if channel == 'gray' else image.copy()
    cv2.rectangle(img_copy, (x1, y1), (x2, y2), (255), 2)
    cv2.imwrite(output_path, img_copy)

    return median_value

# ---------------------- CURVE FITTING ---------------------- #
def barney_curve(x, A, B, C, D):
    return A / (B + (C * np.array(x) + D) ** 3)

def barney_curve_predict_value(pixels, A, B, C, D):
    ppm = (np.cbrt((A / pixels) - B) - D) / C
    ppm = np.clip(ppm, 0.01, 10)  # Keep ppm in [0.01, 10]
    return ppm

def plot_colorimetry_calibration(ppm, pixels, title, dye_index, plots_path):
    """Fit the calibration curve and store parameters."""
    guess = (245, 240, 1.5, 1.1)
    params, cov = curve_fit(barney_curve, ppm, pixels, guess)
    BARNEY_PARAMETERS[dye_index].append(tuple(params))
    
    # Plot
    x_vals = np.arange(0, 10, 0.1)
    y_vals = barney_curve(x_vals, *params)
    fig, ax = plt.subplots()
    ax.set_facecolor('black')
    colors = ["lightgoldenrodyellow", "sandybrown", "yellow", "purple", "lightcoral", "gold"]
    ax.plot(ppm, pixels, 'o', color=colors[dye_index])
    ax.plot(x_vals, y_vals, '--', color=colors[dye_index], alpha=0.6, label=title)
    ax.set_title(title)
    ax.set_xlabel("PPM")
    ax.set_ylabel("Pixel Value")
    plt.grid(color='white', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.savefig(os.path.join(plots_path, f"{title}.jpg"), dpi=400)
    plt.close()

# ---------------------- COLORIMETRY ---------------------- #
def colorimetry(calibration_paths, plots_path):
    dyes = [[] for _ in range(6)]
    ppm_list = [1, 2, 4, 6, 8, 10]

    for i, ppm in enumerate(ppm_list):
        for d in range(6):
            input_img = os.path.join(calibration_paths[d], f"dye{d+1}_{ppm}ppm.jpg")
            output_img = os.path.join(calibration_paths[d], f"ROI_calibration_dye{d+1}_{ppm}_ppm.jpg")
            value = draw_center_square(input_img, output_img, channel=CHANNELS[d])
            dyes[d].append(value)
    
    for d in range(6):
        plot_colorimetry_calibration(ppm_list, dyes[d], f"Dye {d+1} Fitting Curve", d, plots_path)

    # Remove last calibration point (if needed)
    for d in range(6):
        dyes[d].pop()

    return dyes

def colorimetry_samples(samples_path, output_path, material_name):
    dyes = [[] for _ in range(6)]
    for d in range(6):
        input_img = os.path.join(samples_path, f"{material_name}_DYE{d+1}.jpg")
        output_img = os.path.join(output_path, f"ROI_SAMPLE_DYE{d+1}.jpg")
        value = draw_center_square(input_img, output_img, channel=CHANNELS[d])
        dyes[d].append(value)
    return dyes

# ---------------------- PLOTTING ---------------------- #
def plot_with_regression_and_images(calibration_images, sample_images, material_name, results_path):
    """Plot regression lines and sample predictions."""
    dyes = colorimetry_samples(os.path.dirname(sample_images[0]), os.path.dirname(sample_images[0]), material_name)
    ppm_values = [2, 4, 6, 8, 10]
    colors = ["lightgoldenrodyellow", "sandybrown", "yellow", "purple", "lightcoral", "gold"]

    fig = plt.figure(figsize=(16, 8), facecolor='black')
    gs = gridspec.GridSpec(nrows=1, ncols=2, width_ratios=[2, 1.6])
    ax_reg = fig.add_subplot(gs[0, 0])
    ax_reg.set_facecolor('black')
    ax_reg.set_xlim(0, 10)
    ax_reg.set_ylim(0, 300)
    ax_reg.set_xlabel("PPM")
    ax_reg.set_ylabel("Pixel Value")
    ax_reg.set_title(f"Predicted PPMs for {material_name}")

    # Plot regression curves
    for i in range(6):
        A, B, C, D = BARNEY_PARAMETERS[i][0]
        x_vals = np.arange(0, 10, 0.1)
        y_vals = barney_curve(x_vals, A, B, C, D)
        ax_reg.plot(x_vals, y_vals, '--', color=colors[i], label=f"Dye {i+1}", alpha=0.6)
    ax_reg.legend(facecolor='black', edgecolor='white', labelcolor='white')

    plt.tight_layout()
    plt.savefig(os.path.join(results_path, f"{material_name}_RESULTS.jpg"), dpi=400)
    plt.show()

# ---------------------- MAIN ---------------------- #
if __name__ == '__main__':
    try:
        MATERIAL_NAME = sys.argv[1]
    except IndexError:
        MATERIAL_NAME = 'CMP2_a'

    GLOBAL_PATH = os.getcwd()
    CALIBRATION_PATH = os.path.join(GLOBAL_PATH, 'dataset', 'calibration_vials')
    PLOTS_PATH = os.path.join(GLOBAL_PATH, 'plots')
    SAMPLES_PATH = os.path.join(GLOBAL_PATH, 'dataset', MATERIAL_NAME, 'imgs')
    OUTPUT_PATH = os.path.join(GLOBAL_PATH, 'dataset', MATERIAL_NAME, 'ROI_output')
    RESULTS_PATH = os.path.join(GLOBAL_PATH, 'dataset', MATERIAL_NAME)

    DYE_PATHS = [os.path.join(CALIBRATION_PATH, f'dye{i+1}') for i in range(6)]
    sample_images = [os.path.join(SAMPLES_PATH, f"{MATERIAL_NAME}_DYE{i+1}.jpg") for i in range(6)]
    calibration_images = [[os.path.join(DYE_PATHS[d], f"dye{d+1}_{ppm}ppm.jpg") for ppm in [1,2,4,6,8,10]] for d in range(6)]

    # Run plotting
    plot_with_regression_and_images(calibration_images, sample_images, MATERIAL_NAME, RESULTS_PATH)


