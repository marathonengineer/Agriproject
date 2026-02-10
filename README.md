

## Quick Start (Docker)

If you have Docker installed, this is the easiest way to run the analysis.

1.  **Build the Image**:
    ```bash
    docker build -t plantcv-app .
    ```

2.  **Run the Container**:
    Mount your local `data` directory to `/app/data` in the container.
    ```bash
    # Windows (PowerShell)
    docker run -it -v "${PWD}/plantcv_project/data:/app/data" plantcv-app

    # Linux/Mac
    docker run -it -v "$(pwd)/plantcv_project/data:/app/data" plantcv-app
    ```

3.  **Run Analysis**:
    Inside the container:
    ```bash
    python run_analysis.py
    ```

## Local Setup (Python)

If you prefer to run locally without Docker:

1.  **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    ```

2.  **Activate the Virtual Environment**:
    - Windows: `.\venv\Scripts\Activate`
    - Mac/Linux: `source venv/bin/activate`

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Analysis**:
    ```bash
    python run_analysis.py
    ```

## Data Structure

- Place input images in `data/images/`.
- Place binary masks in `data/masks/`.
- Mask filenames must match the image filename with `_mask` appended (e.g., `plant.png` -> `plant_mask.png`).