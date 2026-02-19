# File Structure


data/

raw/.gitkeep — keeps the empty folder tracked by git. Raw data goes here, never modified.
processed/.gitkeep — cleaned and transformed data ready for modeling goes here.
external/.gitkeep — third party data like census data, weather data, etc.


notebooks/

01_eda.ipynb — exploratory data analysis, understanding distributions, missing values, correlations.
02_preprocessing.ipynb — experimenting with cleaning, encoding, scaling before moving to src/.
03_modeling.ipynb — trying out different models, hyperparameters, comparing results.
04_evaluation.ipynb — final model evaluation, confusion matrix, ROC curve, feature importance.


src/data/

__init__.py — makes the folder a Python package so you can import from it.
ingest.py — loads raw data from CSV, database, S3, or API into a dataframe.
preprocess.py — handles cleaning, missing values, encoding, scaling, feature engineering.

src/models/

__init__.py — makes the folder a Python package.
train.py — trains the model, logs metrics, saves the trained model to disk.
predict.py — loads a saved model and runs predictions on new data.
evaluate.py — computes metrics like accuracy, F1, AUC, generates evaluation reports.

src/pipelines/

__init__.py — makes the folder a Python package.
training_pipeline.py — chains ingest → preprocess → train → evaluate into one callable flow.
inference_pipeline.py — chains load model → preprocess input → predict → return result.

src/utils/

__init__.py — makes the folder a Python package.
helpers.py — shared utility functions used across the project like file loaders, timer decorators, custom exceptions.


models/

staging/.gitkeep — candidate models land here after training, waiting to be validated.
production/.gitkeep — only promoted, validated models live here. What the API actually serves.


mlops/tracking/mlflow/

mlruns/.gitkeep — MLflow stores all experiment runs, parameters, metrics, and artifacts here automatically when you log with MLflow.

mlops/monitoring/

data_drift.py — compares incoming live data against training data to detect drift using tools like Evidently or WhyLogs. Alerts you when the data distribution shifts.
model_performance.py — tracks live prediction performance over time. Detects when model accuracy degrades so you know when to retrain.

mlops/serving/api/

app.py — the FastAPI application entry point. Initializes the app, loads the model, starts the server.
schemas.py — Pydantic models defining the exact shape of request and response. For example a request must have age: int, salary: float, and response returns churn_probability: float.
routes.py — defines API endpoints like POST /predict, GET /health, GET /metrics.

mlops/serving/batch/

batch_predict.py — loads a saved model and runs predictions on a full dataset at once. Used for nightly scoring jobs like scoring all customers and writing results back to a database.


pipelines/

training_dag.py — an Airflow/Prefect/ZenML DAG that schedules and orchestrates the full training pipeline automatically, for example every Sunday midnight.
inference_dag.py — a scheduled DAG that runs batch predictions on a schedule, for example every morning at 6am to score new records overnight.


docker/

Dockerfile — containerizes the training code so it runs identically on any machine or cloud environment.
Dockerfile.api — separately containerizes the FastAPI serving app so it can be deployed independently.
docker-compose.yml — defines and runs all services together with one command. For example API server + database + monitoring dashboard all at once with docker-compose up.


.github/workflows/

ci.yml — runs automatically on every pull request. Lints code, runs tests, checks formatting. Blocks merging if anything fails.
cd_staging.yml — automatically deploys to a staging environment when code is merged to the develop branch. Used for testing before production.
cd_production.yml — automatically deploys to production when code is merged to main. Only runs if CI passes.


reports/

figures/.gitkeep — stores all generated plots and visualizations like ROC curves, confusion matrices, feature importance charts.
summary.md — written summary of findings, model performance, business insights, and recommendations.


tests/unit/

test_preprocess.py — unit tests for preprocessing functions. Makes sure encoding, scaling, and cleaning behave correctly with different inputs.
test_model.py — unit tests for model functions. Makes sure train, predict, and evaluate functions work correctly.

tests/integration/

test_api.py — tests the full API end to end. Sends a real request to the FastAPI server and checks the response is correct.


config/

config.yaml — central config for file paths, environment settings, feature column names, target column, train/test split ratio, etc.
model_params.yaml — hyperparameters for your models like n_estimators, max_depth, learning_rate. Keeping them here means you never hardcode them in scripts.
logging.yaml — configures log format, log levels (DEBUG/INFO/WARNING/ERROR), and output destination (console, log file, or both).


Root files

.gitignore — tells git to ignore files like data/raw/, models/, .env, __pycache__, .ipynb_checkpoints so they don't get committed.
requirements.txt — production dependencies. What gets installed in Docker and on the server.
requirements-dev.txt — development only dependencies like pytest, black, flake8, jupyter. Not installed in production.
Makefile — shortcut commands so make train runs training, make test runs tests, make serve starts the API, make lint formats code.
README.md — project overview, setup instructions, how to train the model, how to run the API, project structure explanation.