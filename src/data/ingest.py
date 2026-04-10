import os

import pandas as pd

from src.utils.helpers import CreateFile, load_yaml


class DataIngestion:
    def __init__(self):
        self.config = load_yaml("config/config.yaml")
        self.raw_data_path = self.config["data_ingestion"]["raw_data_path"]
        if not os.path.exists(self.raw_data_path):
            CreateFile(self.raw_data_path)

    def ingest_saved_data_github(self):
        """
        Ingest data from GitHub repository
        """
        df = pd.read_csv(self.config["data_ingestion"]["github_data_path"])
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'],errors='coerce')
        df['TotalCharges'] = df['TotalCharges'].astype(float)
        print("Data ingested from GitHub")
        df.to_csv(self.raw_data_path, index=False)
        print("Data saved locally")

if __name__=="__main__":
    trial = DataIngestion()
    trial.ingest_saved_data_github()