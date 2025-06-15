# We are in /opt/airflow/{dags,etl} directory, so we need to add module search `..``
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.config import CONFIG, setup_logger
logger = setup_logger(name="evaluate")

import argparse

import json
import pickle
import pandas

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

def evaluate(data_path, model_filepath, metrics_path):
    try:
        logger.info(f"Loading file '{data_path}' as pandas dataframe...")
        df = pandas.read_csv(data_path)
        X = df.drop(columns=[CONFIG["target_column"]])
        y = df[CONFIG["target_column"]]
        logger.info("Splitting data (will use test part only)...")
        _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        logger.info(f"Loading model from '{model_filepath}'...")
        with open(model_filepath, 'rb') as file:
            model = pickle.load(file)
        logger.info("Making prediction...")
        y_pred = model.predict(X_test)
        logger.info("Calculating metrics...")
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
            "f1_score": f1_score(y_test, y_pred)
        }
        logger.info(f"Saving metrics to '{metrics_path}'..")
        with open(metrics_path, "w") as f:
            json.dump(metrics, f, indent=4)
        print(metrics)
    except Exception as e:
        logger.critical(f"Failed to evaluate model. Exception: {e}.")
        raise e
    logger.info(f"Metrics are calculated and saved.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default=CONFIG["data_filepath"])
    parser.add_argument("--model", type=str, default=CONFIG["model_filepath"])
    parser.add_argument("--metrics", type=str, default=CONFIG["metrics_path"])
    args = parser.parse_args()

    evaluate(args.data, args.model, args.metrics)