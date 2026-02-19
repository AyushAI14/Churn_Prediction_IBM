import os
from src.utils.helpers import CreateFile, load_yaml
import joblib as jb
from sklearn.metrics import  confusion_matrix,classification_report
import pandas as pd
from sklearn.model_selection import train_test_split

class ModelEvaluation:
    def __init__(self):
        self.config = load_yaml("config/config.yaml")
        self.model_path = self.config["model_training"]["model_path"]
        self.model = jb.load(self.model_path)
        self.process_data_path = self.config["data_preprocessing"]["processed_data_path"]
        if not os.path.exists(self.process_data_path):
            CreateFile(self.process_data_path)
    

    def evaluate_model(self):
        main_df = pd.read_csv(self.process_data_path)
        X = main_df.drop(columns=['customerID','Churn'])
        y = main_df['Churn']
        print("Data loaded successfully")
        
        X_train,X_test,Y_train,Y_test=train_test_split(X,y,stratify=y,random_state=42)
        print("Data split successfully")

        y_pred = self.model.predict(X_test)
        cm = confusion_matrix(Y_test, y_pred)
        cr = classification_report(Y_test, y_pred)
        print("Confusion Matrix:\n", cm)
        print("Classification Report:\n", cr)
        

# trial = ModelEvaluation()
# trial.evaluate_model()