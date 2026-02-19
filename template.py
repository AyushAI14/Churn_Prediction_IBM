import os
from pathlib import Path

project_name = "my_ml_project"
src_folder = "src"
mlops_folder = "mlops"
pipelines_folder = "pipelines"
docker_folder = "docker"
config_folder = "config"
tests_folder = "tests"
notebooks_folder = "notebooks"
reports_folder = "reports"
data_folder = "data"
models_folder = "models"

list_of_files = [
    # Data
    f"{data_folder}/raw/.gitkeep",
    f"{data_folder}/processed/.gitkeep",

    # Notebooks
    f"{notebooks_folder}/01_experiement.ipynb",

    # src
    f"{src_folder}/__init__.py",
    f"{src_folder}/data/__init__.py",
    f"{src_folder}/data/ingest.py",
    f"{src_folder}/data/preprocess.py",
    f"{src_folder}/models/__init__.py",
    f"{src_folder}/models/train.py",
    f"{src_folder}/models/predict.py",
    f"{src_folder}/models/evaluate.py",
    f"{src_folder}/pipelines/__init__.py",
    f"{src_folder}/pipelines/training_pipeline.py",
    f"{src_folder}/pipelines/inference_pipeline.py",
    f"{src_folder}/utils/__init__.py",
    f"{src_folder}/utils/helpers.py",

    # Models
    f"{models_folder}/staging/.gitkeep",
    f"{models_folder}/production/.gitkeep",

    # MLOps - Tracking
    f"{mlops_folder}/tracking/mlflow/mlruns/.gitkeep",

    # MLOps - Monitoring
    # f"{mlops_folder}/monitoring/data_drift.py",
    # f"{mlops_folder}/monitoring/model_performance.py",

    # MLOps - Serving
    f"{mlops_folder}/serving/api/app.py",
    f"{mlops_folder}/serving/batch/batch_predict.py",

    # # Pipelines (orchestration)
    # f"{pipelines_folder}/training_dag.py",
    # f"{pipelines_folder}/inference_dag.py",

    # Docker
    f"{docker_folder}/Dockerfile",
    f"{docker_folder}/Dockerfile.api",
    f"{docker_folder}/docker-compose.yml",

    # CI/CD
    ".github/workflows/ci.yml",
    ".github/workflows/cd_staging.yml",
    ".github/workflows/cd_production.yml",

    # Reports
    f"{reports_folder}/figures/.gitkeep",
    f"{reports_folder}/summary.md",

    # Tests
    f"{tests_folder}/unit/test_preprocess.py",
    f"{tests_folder}/unit/test_model.py",
    f"{tests_folder}/integration/test_api.py",

    # Config
    f"{config_folder}/config.yaml",
    f"{config_folder}/model_params.yaml",

    # Root
    ".gitignore",
    "requirements.txt",
    "requirements-dev.txt",
    "Makefile",
    "README.md",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir = filepath.parent
    
    if not filedir.exists():
        os.makedirs(filedir,exist_ok=True)
    if not filepath.exists() or filepath.stat().st_size == 0:
        filepath.touch()
        print(f"File {filepath} created")
    else:
        print(f"File {filepath} already exists")