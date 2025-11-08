# 🧩 **`pipeline/` README — Training Pipeline**

This folder contains the **workflow orchestration layer** for the **MLOps Machine Maintenance** project.
It connects the core components of the system — **data preprocessing** and **model training** — into a single, streamlined execution flow.

The entry point of this folder is `training_pipeline.py`, which automates the **end-to-end workflow** from raw data ingestion to model evaluation.

## ⚙️ **Purpose**

The `training_pipeline.py` module serves as the **controller** of the MLOps workflow.
It ensures that each major stage of the project — **data processing** and **model training** — runs sequentially, reproducibly, and with clear logging and error handling.

### 🎯 Key Objectives

* Automate the **full ML lifecycle** from data preparation to model evaluation
* Provide **reproducible execution** using consistent inputs and outputs
* Centralise logging and exception handling for debugging and monitoring
* Create a **foundation for future CI/CD integration** (Kubeflow, Airflow, GitHub Actions)

## 📁 **Folder Structure**

```text
pipeline/
└── training_pipeline.py    # 🚀 Orchestrates data processing → model training → evaluation
```

## 🧠 **Workflow Overview**

### 🔄 End-to-End Execution Flow

| Stage | Component                              | Description                                                                                             |
| ----: | -------------------------------------- | ------------------------------------------------------------------------------------------------------- |
|   1️⃣ | **Data Processing** (`DataProcessing`) | Loads raw machine sensor data, performs cleaning, encoding, scaling, and saves processed splits.        |
|   2️⃣ | **Model Training** (`ModelTraining`)   | Loads processed data, trains a Logistic Regression model, saves the model, and logs evaluation metrics. |

Both stages leverage:

* `src/logger.py` for unified logging
* `src/custom_exception.py` for consistent error handling

## 🧩 **`training_pipeline.py` — Overview**

The file runs the two workflow stages in sequence:

```python
from src.data_processing import DataProcessing
from src.model_training import ModelTraining

if __name__ == "__main__":
    # Stage 1: Data Preprocessing
    processor = DataProcessing("artifacts/raw/data.csv", "artifacts/processed")
    processor.run()

    # Stage 2: Model Training & Evaluation
    trainer = ModelTraining("artifacts/processed/", "artifacts/models/")
    trainer.run()
```

## 🧰 **How to Run the Pipeline**

Make sure your environment is activated and your raw dataset exists at `artifacts/raw/data.csv`.
Then, from the project root directory, execute:

```bash
python pipeline/training_pipeline.py
```

### ✅ Expected Output (Console Logs)

```console
2025-11-08 14:15:21,345 - INFO - Data processing initialised.
2025-11-08 14:15:22,119 - INFO - Basic data preprocessing completed.
2025-11-08 14:15:22,601 - INFO - Train/test splits and scaler saved successfully.
2025-11-08 14:15:23,005 - INFO - Model training initialised.
2025-11-08 14:15:23,422 - INFO - Model trained and saved successfully.
2025-11-08 14:15:23,873 - INFO - Accuracy : 0.85 ; Precision : 0.84 ; Recall : 0.85 ; F1 : 0.84
2025-11-08 14:15:24,012 - INFO - End-to-end pipeline completed successfully.
```

This confirms that:

* Data preprocessing and model training were executed in sequence
* Processed data and model artefacts were saved correctly
* Evaluation metrics were computed and logged clearly

## 🧩 **Integration with MLOps Components**

| Stage           | Source Module             | Output Location           | Description                          |
| --------------- | ------------------------- | ------------------------- | ------------------------------------ |
| Data Processing | `src/data_processing.py`  | `artifacts/processed/`    | Saves preprocessed splits and scaler |
| Model Training  | `src/model_training.py`   | `artifacts/models/`       | Saves trained model (`model.pkl`)    |
| Logging         | `src/logger.py`           | `logs/log_YYYY-MM-DD.log` | Timestamped logs for traceability    |
| Error Handling  | `src/custom_exception.py` | Console & logs            | Standardised exception messages      |

## 🧱 **Future Extensions**

The `pipeline/` directory is designed to evolve into a **production-ready orchestration layer**, supporting:

* ✅ CI/CD integration (GitHub Actions, Jenkins, or CircleCI)
* ☁️ Cloud pipeline automation (Kubeflow, Vertex AI, or Airflow)
* 📊 Monitoring hooks for model drift detection and retraining triggers
* 🧩 Scalable multi-stage workflows for data validation, evaluation, and deployment

## ✅ **In Summary**

`training_pipeline.py` provides a **clean, modular, and automated orchestration script** that links all major stages of the **MLOps Machine Maintenance** workflow.
It forms the backbone for scaling this project into a **fully automated, production-grade MLOps pipeline**, ensuring **reproducibility, traceability, and maintainability** across all stages.
