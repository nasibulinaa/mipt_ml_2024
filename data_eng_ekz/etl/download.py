# We are in /opt/airflow/{dags,etl} directory, so we need to add module search `..``
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.config import CONFIG, setup_logger
logger = setup_logger(name="download")

import argparse

import urllib.request
from etl.config import CONFIG, setup_logger
logger = setup_logger(name="download")

def download_and_save(output_path):
    try:
        logger.info("Downloading data...")
        urllib.request.urlretrieve(CONFIG["dataset_url"], output_path)
    except Exception as e:
        logger.critical(f"Failed to download dataset.")
        raise e
    logger.info(f"Data is succesfully downloaded and saved to {output_path}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-path", type=str, default=CONFIG["raw_data_filepath"])
    args = parser.parse_args()
    download_and_save(args.output_path)
