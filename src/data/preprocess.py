import os
import pandas as pd
from src.utils.helpers import CreateFile, load_yaml,CommonEdaMetrics
from sklearn.preprocessing import OneHotEncoder
import joblib



class DataProcessing:
    def __init__(self):
        self.config = load_yaml("config/config.yaml")
        self.df = pd.read_csv(self.config['data_ingestion']['raw_data_path'])
        self.process_data_path = self.config["data_preprocessing"]["processed_data_path"]
        if not os.path.exists(self.process_data_path):
            CreateFile(self.process_data_path)
        
    def eda_image(self):
        pass
    def FeatureEngineering(self):
        """
        This function performs feature engineering on the ingested data.
        """
        df = self.df
        print("Raw Data Loaded")
        
        nominal_cols = [
            'gender',
            'Partner',
            'Dependents',
            'PhoneService',
            'MultipleLines',
            'InternetService',
            'OnlineSecurity',
            'OnlineBackup',
            'DeviceProtection',
            'TechSupport',
            'StreamingTV',
            'StreamingMovies',
            'PaperlessBilling',
            'PaymentMethod'
        ]
        
        # ordinal encoding and target var
        df['Churn']=df['Churn'].map({'Yes': 1, 'No': 0})
        df['Contract']=df['Contract'].map({'One year': 1, 'Month-to-month': 0, 'Two year': 2})
        

        # nominal encoding
        ohe = OneHotEncoder(drop='first',sparse_output=False)
        encoded = ohe.fit_transform(df[nominal_cols])
        joblib.dump(ohe, self.config["data_preprocessing"]["encoder_path"])
        encorded_df = pd.DataFrame(encoded,columns=ohe.get_feature_names_out(nominal_cols),index=df.index)
        # print(df.shape)
        df.drop(columns=nominal_cols,inplace=True)
        # print(df.shape)
        main_df = pd.concat([df,encorded_df],axis=1)
        
        # save the processed data
        main_df.to_csv(self.process_data_path,index=False)
        print("Processed data saved to",self.process_data_path)
        # return CommonEdaMetrics(self.config["data_preprocessing"]["processed_data_path"])
        

# trial = DataProcessing()
# trial.FeatureEngineering()