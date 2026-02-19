import os
from xgboost import XGBClassifier
import pandas as pd
from src.utils.helpers import CreateFile, load_yaml
import joblib as jb
from sklearn.model_selection import train_test_split
from sklearn.metrics import  confusion_matrix


class ModelTraining:
    def __init__(self):
        self.config = load_yaml("config/config.yaml")
        self.model_params = load_yaml("config/model_params.yaml")
        self.process_data_path = self.config["data_preprocessing"]["processed_data_path"]
        if not os.path.exists(self.process_data_path):
            CreateFile(self.process_data_path)

    def train_model(self):
        # Load the processed data
        main_df = pd.read_csv(self.process_data_path)
        X = main_df.drop(columns=['customerID','Churn'])
        y = main_df['Churn']
        print("Data loaded successfully")
        
        X_train,X_test,Y_train,Y_test=train_test_split(X,y,stratify=y,random_state=42)
        print("Data split successfully")
        
        xg = XGBClassifier(
            scale_pos_weight=self.model_params["model"]["scale_pos_weight"],
            n_estimators=self.model_params["model"]["n_estimators"],
            max_depth=self.model_params["model"]["max_depth"],
            learning_rate=self.model_params["model"]["learning_rate"],
            eval_metric=self.model_params["model"]["eval_metric"],
            random_state=self.model_params["model"]["random_state"],
            colsample_bytree=self.model_params["model"]["colsample_bytree"],
            subsample=self.model_params["model"]["subsample"],
            verbosity=1
        )
        
        xg.fit(X_train,Y_train,verbose=True)
        print("Model trained successfully")
        xg_p = xg.predict(X_test)
        jb.dump(xg, self.config["model_training"]["model_path"])
        print("Model saved successfully")

# trail = ModelTraining()
# trail.train_model()