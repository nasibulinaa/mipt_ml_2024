import os
import sys
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

for dir in [BASE_DIR, LOGS_DIR, DATA_DIR, RESULTS_DIR]:
    os.makedirs(LOGS_DIR, exist_ok=True)

CONFIG = {
    "raw_data_filepath": os.path.join(DATA_DIR, "raw_data.csv"),
    "data_filepath": os.path.join(DATA_DIR, "ready_data.csv"),
    "model_filepath": os.path.join(RESULTS_DIR, "model.pkl"),
    "metrics_path": os.path.join(RESULTS_DIR, "metrics.json"),
    "dataset_url": "https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wdbc.data",
    # https://www.kaggle.com/datasets/uciml/breast-cancer-wisconsin-data/data
    "header": [
        "id",
        "diagnosis",
        "radius_mean",
        "texture_mean",
        "perimeter_mean",
        "area_mean",
        "smoothness_mean",
        "compactness_mean",
        "concavity_mean",
        "concave points_mean",
        "symmetry_mean",
        "fractal_dimension_mean",
        "radius_se",
        "texture_se",
        "perimeter_se",
        "area_se",
        "smoothness_se",
        "compactness_se",
        "concavity_se",
        "concave points_se",
        "symmetry_se",
        "fractal_dimension_se",
        "radius_worst",
        "texture_worst",
        "perimeter_worst",
        "area_worst",
        "smoothness_worst",
        "compactness_worst",
        "concavity_worst",
        "concave points_worst",
        "symmetry_worst",
        "fractal_dimension_worst",
    ],
    "target_column": "diagnosis",
}


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    # PythonOperator adds logger itself
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    log_file = os.path.join(LOGS_DIR, f"{name}.log")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
