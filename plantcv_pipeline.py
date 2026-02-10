import os
import cv2
import numpy as np
import pandas as pd
import plantcv as pcv

def load_image_and_mask(image_path, mask_path):
    img, path, filename = pcv.readimage(image_path)
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    mask = np.where(mask > 127, 255, 0).astype(np.uint8)
    return img, mask

def compute_leaf_color(img, mask):
    color_stats = pcv.analyze_color(img, mask, hist_plot_type=None)
    mean_green = float(np.mean(img[:, :, 1][mask == 255]))
    return mean_green

def compute_leaf_area(mask, pixel_to_cm2=None):
    area_pixels = np.sum(mask == 255)

    if pixel_to_cm2:
        return area_pixels * pixel_to_cm2
    return area_pixels

def compute_curl_index(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return 0.0

    cnt = max(contours, key=cv2.contourArea)
    perimeter = cv2.arcLength(cnt, True)
    area = cv2.contourArea(cnt)

    if area == 0:
        return 0.0

    curl_index = perimeter / (2 * np.sqrt(np.pi * area))
    return float(curl_index)

def compute_plant_height(mask, pixel_to_cm=None):
    ys, xs = np.where(mask == 255)

    if len(ys) == 0:
        return 0.0

    height_pixels = max(ys) - min(ys)

    if pixel_to_cm:
        return height_pixels * pixel_to_cm
    return height_pixels

def analyze_single_plant(image_path, mask_path, pixel_to_cm=None, pixel_to_cm2=None):
    img, mask = load_image_and_mask(image_path, mask_path)

    leaf_color = compute_leaf_color(img, mask)
    leaf_area = compute_leaf_area(mask, pixel_to_cm2)
    curl_index = compute_curl_index(mask)
    plant_height = compute_plant_height(mask, pixel_to_cm)

    return {
        "image": os.path.basename(image_path),
        "leaf_green_mean": leaf_color,
        "leaf_area": leaf_area,
        "curl_index": curl_index,
        "plant_height": plant_height
    }