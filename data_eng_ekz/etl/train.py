# We are in /opt/airflow/{dags,etl} directory, so we need to add module search `..``
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.config import CONFIG, setup_logger
logger = setup_logger(name="train")

import argparse

import pickle
import pandas
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def train(data_path, model_filepath):
    # https://www.geeksforgeeks.org/machine-learning/ml-kaggle-breast-cancer-wisconsin-diagnosis-using-logistic-regression/
    try:
        logger.info(f"Loading file '{data_path}' as pandas dataframe...")
        df = pandas.read_csv(data_path)
        logger.info(f"File loaded: {df.shape[0]} lines and {df.shape[1]} columns.")
        target_column = CONFIG["target_column"]
        X, y = df.drop(columns=[target_column]), df[target_column]
        logger.info("Splitting data (will use train part only)...")
        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
        logger.info(f"Shape of train part: {X_train.shape}")
        logger.info("Preparation done. Now doing real training...")
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)
        logger.info("Training of model done. Saving model...")
        with open(model_filepath, 'wb') as file:
            pickle.dump(model, file)
    except Exception as e:
        logger.critical(f"Failed to train model. Exception: {e}.")
        raise e
    logger.info(f"Trained model saved to {model_filepath}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default=CONFIG["data_filepath"])
    parser.add_argument("--model", type=str, default=CONFIG["model_filepath"])
    args = parser.parse_args()

    train(args.data, args.model)
