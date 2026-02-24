import os
import cv2
import numpy as np
import pandas as pd
import plantcv.plantcv as pcv

def load_image_and_mask(image_path, mask_path):
    img, path, filename = pcv.readimage(image_path)
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    if np.max(mask) == 1:
        mask = (mask * 255).astype(np.uint8)
    else:
        mask = np.where(mask > 127, 255, 0).astype(np.uint8)
    return img, mask

def compute_leaf_color(img, mask):
    # Extracts the mean of the Green channel where the mask is active
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

    # Curl Index (Circularity): 1.0 is a perfect circle, higher indicates irregular/curled edges
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

def classify_plant_health(green, area, curl, height):
    """
    Calculates a health score (0-1) and assigns a category.
    Adjust thresholds below based on your specific plant species observed norms.
    """
    # 1. Greenness Score (Max 0.4): Healthy plants usually > 150 in green channel
    s_green = min(green / 150, 1.0) * 0.4
    
    # 2. Area Score (Max 0.3): Adjust '2000' based on your average healthy plant size
    s_area = min(area / 2000, 1.0) * 0.3
    
    # 3. Curl Penalty (Max 0.15): 1.0 is healthy, > 2.0 indicates severe wilting/curling
    s_curl = max(0, 1 - (curl - 1) / 1.5) * 0.15
    
    # 4. Height Score (Max 0.15): Adjust '500' based on your camera distance/zoom
    s_height = min(height / 500, 1.0) * 0.15

    total_score = s_green + s_area + s_curl + s_height

    if total_score > 0.75:
        return "Good", total_score
    elif total_score > 0.45:
        return "Moderate", total_score
    else:
        return "Severe", total_score

def analyze_single_plant(image_path, mask_path, pixel_to_cm=None, pixel_to_cm2=None):
    img, mask = load_image_and_mask(image_path, mask_path)

    # Core Metric Extraction
    leaf_color = compute_leaf_color(img, mask)
    leaf_area = compute_leaf_area(mask, pixel_to_cm2)
    curl_index = compute_curl_index(mask)
    plant_height = compute_plant_height(mask, pixel_to_cm)

    # Health Classification
    category, score = classify_plant_health(leaf_color, leaf_area, curl_index, plant_height)

    area_unit = "cm2" if pixel_to_cm2 else "pixels"
    height_unit = "cm" if pixel_to_cm else "pixels"

    return {
        "image": os.path.basename(image_path),
        "leaf_green_mean": round(leaf_color, 2),
        f"leaf_area_{area_unit}": round(leaf_area, 2),
        "curl_index": round(curl_index, 3),
        f"plant_height_{height_unit}": round(plant_height, 2),
        "health_category": category,
        "health_score": round(score, 3)
    }
