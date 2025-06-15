# We are in /opt/airflow/{dags,etl} directory, so we need to add module search `..``
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.config import CONFIG, setup_logger
logger = setup_logger(name="upload")

import argparse

def upload(model_path, metrics_path):
    try:
        pass
    except Exception as e:
        logger.critical(f"Failed to upload.")
        raise e
    logger.info(f"Data is succesfully uploaded.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default=CONFIG["model_filepath"])
    parser.add_argument("--metrics", type=str, default=CONFIG["metrics_path"])
    args = parser.parse_args()
    upload(args.model, args.metrics)
