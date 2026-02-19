import joblib as jb
import pandas as pd
from src.utils.helpers import load_yaml
from sklearn.preprocessing import OneHotEncoder


class Prediction:
    def __init__(self):
        self.config = load_yaml("config/config.yaml")
        self.model = jb.load(self.config['model_training']['model_path'])
        pd.set_option('display.max_rows', None)

        
    def preprocessing(self,df):
        print("Preprocessing start for prediction")
        
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
        # df['Churn']=df['Churn'].map({'Yes': 1, 'No': 0})
        df['Contract']=df['Contract'].map({'One year': 1, 'Month-to-month': 0, 'Two year': 2})
        

        # nominal encoding
        ohe = jb.load(self.config["data_preprocessing"]["encoder_path"])
        encoded = ohe.transform(df[nominal_cols])
        encorded_df = pd.DataFrame(encoded,columns=ohe.get_feature_names_out(nominal_cols),index=df.index)
        # print(df.shape)
        df.drop(columns=nominal_cols,inplace=True)
        # print(df.shape)
        main_df = pd.concat([df,encorded_df],axis=1)
        print("Preprocessing Done for prediction")
        print(main_df)
        return main_df
    
    def terminal_df(self):
        data = {}
        
        print("Gender: 1=Female, 2=Male")
        data['gender'] = 'Female' if input("Enter: ") == '1' else 'Male'
        
        print("SeniorCitizen: 1=No, 2=Yes")
        data['SeniorCitizen'] = 0 if input("Enter: ") == '1' else 1
        
        print("Partner: 1=Yes, 2=No")
        data['Partner'] = 'Yes' if input("Enter: ") == '1' else 'No'
        
        print("Dependents: 1=Yes, 2=No")
        data['Dependents'] = 'Yes' if input("Enter: ") == '1' else 'No'
        
        data['tenure'] = int(input("Tenure (months, 0-72): "))
        
        print("PhoneService: 1=Yes, 2=No")
        data['PhoneService'] = 'Yes' if input("Enter: ") == '1' else 'No'
        
        print("MultipleLines: 1=No phone service, 2=No, 3=Yes")
        ml = input("Enter: ")
        data['MultipleLines'] = {'1': 'No phone service', '2': 'No', '3': 'Yes'}[ml]
        
        print("InternetService: 1=DSL, 2=Fiber optic, 3=No")
        isp = input("Enter: ")
        data['InternetService'] = {'1': 'DSL', '2': 'Fiber optic', '3': 'No'}[isp]
        
        print("OnlineSecurity: 1=No, 2=Yes, 3=No internet service")
        os_ = input("Enter: ")
        data['OnlineSecurity'] = {'1': 'No', '2': 'Yes', '3': 'No internet service'}[os_]
        
        print("OnlineBackup: 1=Yes, 2=No, 3=No internet service")
        ob = input("Enter: ")
        data['OnlineBackup'] = {'1': 'Yes', '2': 'No', '3': 'No internet service'}[ob]
        
        print("DeviceProtection: 1=No, 2=Yes, 3=No internet service")
        dp = input("Enter: ")
        data['DeviceProtection'] = {'1': 'No', '2': 'Yes', '3': 'No internet service'}[dp]
        
        print("TechSupport: 1=No, 2=Yes, 3=No internet service")
        ts = input("Enter: ")
        data['TechSupport'] = {'1': 'No', '2': 'Yes', '3': 'No internet service'}[ts]
        
        print("StreamingTV: 1=No, 2=Yes, 3=No internet service")
        stv = input("Enter: ")
        data['StreamingTV'] = {'1': 'No', '2': 'Yes', '3': 'No internet service'}[stv]
        
        print("StreamingMovies: 1=No, 2=Yes, 3=No internet service")
        sm = input("Enter: ")
        data['StreamingMovies'] = {'1': 'No', '2': 'Yes', '3': 'No internet service'}[sm]
        
        print("Contract: 1=Month-to-month, 2=One year, 3=Two year")
        ct = input("Enter: ")
        data['Contract'] = {'1': 'Month-to-month', '2': 'One year', '3': 'Two year'}[ct]
        
        print("PaperlessBilling: 1=Yes, 2=No")
        data['PaperlessBilling'] = 'Yes' if input("Enter: ") == '1' else 'No'
        
        print("PaymentMethod: 1=Electronic check, 2=Mailed check, 3=Bank transfer (automatic), 4=Credit card (automatic)")
        pm = input("Enter: ")
        data['PaymentMethod'] = {'1': 'Electronic check', '2': 'Mailed check', '3': 'Bank transfer (automatic)', '4': 'Credit card (automatic)'}[pm]
        
        data['MonthlyCharges'] = float(input("MonthlyCharges: "))
        data['TotalCharges'] = float(input("TotalCharges: "))
        
        print("\nCollected Data:")
        print(pd.DataFrame([data]))
        
        return pd.DataFrame([data])
        
    def predict(self,df=None):
        if df is None:
            df = self.terminal_df()
        main_df = self.preprocessing(df)
        print(main_df.head())
        print(main_df.shape)
        model = self.model
        print("model loaded")
        yp = model.predict(main_df)
        if yp == 1:
            print("The Customer will Churn")
        else:
            print("The Customer is Likely Loyal")
        
        
    
    
# trial = Prediction()
# # trial.terminal_df()
# trial.predict()