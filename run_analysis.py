import os
import glob
import pandas as pd
from plantcv_pipeline import analyze_single_plant

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(SCRIPT_DIR, "data", "images")
MASK_DIR = os.path.join(SCRIPT_DIR, "data", "masks")
OUTPUT_CSV = "plant_traits.csv"

# --- SET SCALE IF YOU HAVE A RULER IN IMAGE ---
PIXEL_TO_CM = None      # example: 0.05 if 20 pixels = 1 cm
PIXEL_TO_CM2 = None     # example: 0.0025 if 400 px = 1 cm^2

results = []

# Handle both png and jpg
image_extensions = ["*.png", "*.jpg", "*.jpeg"]
image_files = []
for ext in image_extensions:
    image_files.extend(glob.glob(os.path.join(IMAGE_DIR, ext)))

for img_path in image_files:
    filename = os.path.basename(img_path)
    base, _ = os.path.splitext(filename)
    mask_path = os.path.join(MASK_DIR, base + "_mask.png")

    if not os.path.exists(mask_path):
        print(f"Missing mask for {base} (expected: {os.path.basename(mask_path)}), skipping.")
        continue

    metrics = analyze_single_plant(
        img_path,
        mask_path,
        pixel_to_cm=PIXEL_TO_CM,
        pixel_to_cm2=PIXEL_TO_CM2
    )

    results.append(metrics)
    print(f"Processed: {base}")

df = pd.DataFrame(results)
df.to_csv(OUTPUT_CSV, index=False)

print(f"\nSaved results to {OUTPUT_CSV}")
print(df.head())