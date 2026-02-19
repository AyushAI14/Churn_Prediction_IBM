import os
from pathlib import Path
import yaml
import pandas as pd
from sklearn.model_selection import train_test_split

def CreateFile(filepath):
    filepath = Path(filepath)
    filedir = filepath.parent
    
    if not filedir.exists():
        os.makedirs(filedir,exist_ok=True)
    if not filepath.exists() or filepath.stat().st_size == 0:
        filepath.touch()
        print(f"File {filepath} created")
    else:
        print(f"File {filepath} already exists")
        

def load_yaml(filepath):
    with open(filepath,'r') as f:
        return yaml.safe_load(f)
        print("Yaml Loaded")
        

def CommonEdaMetrics(filepath):
    df = pd.read_csv(filepath)
    print("--------------- EDA Metrics ----------- ")
    print("Shape:", df.shape)
    print("Columns:", df.columns)
    print("Data Types:", df.dtypes)
    print("Missing Values:", df.isnull().sum().sum())
    print("Summary Statistics:", df.describe())
    print("Value Counts:", df['Churn'].value_counts())

