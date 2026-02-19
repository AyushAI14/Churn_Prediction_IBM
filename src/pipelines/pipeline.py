from src.data.ingest import DataIngestion
from src.data.preprocess import DataProcessing
from src.models.train import ModelTraining
from src.models.evaluate import ModelEvaluation
from src.models.predict import Prediction


def run_pipeline():

    print("=" * 50)
    print("Step 1: Data Ingestion")
    print("=" * 50)
    ingestion = DataIngestion()
    ingestion.ingest_saved_data_github()

    print("=" * 50)
    print("Step 2: Data Processing")
    print("=" * 50)
    processing = DataProcessing()
    processing.FeatureEngineering()

    print("=" * 50)
    print("Step 3: Model Training")
    print("=" * 50)
    training = ModelTraining()
    training.train_model()

    print("=" * 50)
    print("Step 4: Model Evaluation")
    print("=" * 50)
    evaluation = ModelEvaluation()
    evaluation.evaluate_model()

    print("=" * 50)
    print("Step 5: Prediction")
    print("=" * 50)
    prediction = Prediction()
    prediction.predict()

    print("=" * 50)
    print("Pipeline Completed Successfully!")
    print("=" * 50)


if __name__ == "__main__":
    run_pipeline()