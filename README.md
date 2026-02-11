# PlantCV Analysis Pipeline

This project uses PlantCV to analyze plant images and extract traits such as leaf area, color (greenness), curl index, and height.

## Quick Start (Docker)

To run the analysis using Docker:

1.  **Build the Image**:
    ```bash
    docker build -t plantcv-app .
    ```

2.  **Run the Container**:
    Mount your local `data` directory to `/app/data` in the container.
    ```bash
    docker run --rm -it -v "${PWD}:/app" plantcv-app bash
    ```

3.  **Run Analysis**:
    Inside the container:
    ```bash
    python run_analysis.py
    ```
4.  **Run In A Single Step**:
    ```bash
    docker run --rm -v "${PWD}:/app" plantcv-app python run_analysis.py
    ```
5.  **View Results**:
    The results will be saved to `plant_traits.csv` in the container.
    ```bash
    cat plant_traits.csv
    ```


## Data Structure

- Place input images in `data/images/`.
- Place binary masks in `data/masks/`.
- Mask filenames must match the image filename with `_mask` appended (e.g., `plant.png` -> `plant_mask.png`).

## Configuration

- **Trait Logic**: Functions for trait extraction are located in `plantcv_pipeline.py`.
- **Scaling**: You can adjust `PIXEL_TO_CM` and `PIXEL_TO_CM2` in `run_analysis.py` to convert pixel values to real-world units if known.