# Churn Prediction (IBM Telco Dataset)

This project aims to build an end-to-end churn prediction workflow using the IBM Telco Customer Churn dataset.

## Current Project Status

**Overall completion estimate: ~65%**

The core machine learning pipeline is implemented and runnable from ingestion to prediction, but MLOps serving/testing/documentation pieces are still incomplete.

### Progress by area

| Area | Status | Completion |
|---|---|---:|
| Data ingestion | Implemented (`DataIngestion`) | 100% |
| Data preprocessing / feature engineering | Implemented (`DataProcessing`) | 90% |
| Model training | Implemented (`ModelTraining` with XGBoost) | 90% |
| Model evaluation | Implemented (`ModelEvaluation`) | 85% |
| Prediction workflow (CLI-style input) | Implemented (`Prediction`) | 85% |
| End-to-end orchestration pipeline | Implemented (`run_pipeline`) | 90% |
| FastAPI serving layer | Placeholder file exists, not implemented | 10% |
| Batch serving | Placeholder file exists, not implemented | 10% |
| Automated tests | Test files exist but currently empty | 5% |
| Reporting and docs | Basic structure available, minimal content | 35% |

## What is already done

- Config-driven pipeline setup via YAML files in `config/`.
- Data ingestion from the public IBM GitHub CSV source.
- Feature engineering with:
  - label/ordinal encoding for `Churn` and `Contract`
  - one-hot encoding for nominal features
  - encoder artifact persistence (`.pkl`)
- Model training using `XGBClassifier`.
- Basic model evaluation with confusion matrix and classification report.
- Terminal-based prediction input flow.
- A single orchestrated pipeline script chaining all steps.

## What is pending

- Implement FastAPI app in `mlops/serving/api/app.py`.
- Implement batch prediction job in `mlops/serving/batch/batch_predict.py`.
- Add robust unit and integration tests (`tests/unit`, `tests/integration`).
- Improve experiment tracking and model versioning.
- Add CI checks (lint + test + formatting).
- Expand project reporting (`reports/summary.md`) with metrics and business insights.

## Project Structure

```text
src/
  data/
    ingest.py
    preprocess.py
  models/
    train.py
    evaluate.py
    predict.py
  pipelines/
    pipeline.py
  utils/
    helpers.py

config/
  config.yaml
  model_params.yaml

mlops/
  serving/
    api/app.py
    batch/batch_predict.py

tests/
  unit/
  integration/
```

## How to run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the pipeline:

```bash
python -m src.pipelines.pipeline
```

> Note: The final prediction step currently expects interactive terminal input.

## Immediate next milestones

1. Build a `/predict` API endpoint (Pydantic request/response).
2. Add test coverage for preprocessing and model prediction.
3. Add model evaluation artifact outputs (metrics file + plots).
4. Dockerize and verify API serving path.

---

If you want, I can next convert this status into a checklist roadmap with weekly milestones (Week 1/2/3) and acceptance criteria for each item.
