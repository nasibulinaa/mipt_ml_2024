# We are in /opt/airflow/{dags,etl} directory, so we need to add module search `..``
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.config import CONFIG, setup_logger
logger = setup_logger(name="preprocess")

import argparse

import pandas
from sklearn.preprocessing import StandardScaler

def preprocess(input_path, output_path):
    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file {input_path} not found.")
        logger.info(f"Loading file '{input_path}' as pandas dataframe...")
        df = pandas.read_csv(input_path, header=None, names=CONFIG["header"])
        logger.info(f"File loaded: {df.shape[0]} lines and {df.shape[1]} columns.")
        df=df.drop(columns=["id"])
        target_column = CONFIG["target_column"]
        logger.info(f"Now doing validation...")
        if df.isnull().any().any():
            raise ValueError("Data has null values.")
        if target_column not in df.columns:
            raise AttributeError(f"Target column '{target_column}' not found in dataset.")
        df = df.drop(columns=["target"], errors="ignore")
        df[target_column] = df[target_column].map({"B": 0, "M": 1})
        if df[target_column].isnull().any():
            raise AttributeError(f"Failed to map target values.")
        X, y = df.drop(columns=[target_column]), df[target_column]
        logger.info("Validation done. Now doing scale...")
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        if X_scaled.shape != X.shape:
            logger.warning(f"Scaled shape ({X_scaled.shape}) differs from original one ({X.shape}).")
        logger.info("Saving data...")
        df_scaled = pandas.DataFrame(X_scaled, columns=X.columns)
        df_scaled[target_column] = y.values
        df_scaled.to_csv(output_path, index=False)
    except Exception as e:
        logger.critical(f"Failed to preprocess dataset. Exception: {e}")
        raise e
    logger.info(f"Preprocessed data saved to {output_path}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default=CONFIG["raw_data_filepath"])
    parser.add_argument("--output", type=str, default=CONFIG["data_filepath"])
    args = parser.parse_args()

    preprocess(args.input, args.output)
