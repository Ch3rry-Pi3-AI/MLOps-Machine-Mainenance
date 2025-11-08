# 🚀 **Training Pipeline — MLOps Machine Maintenance**

This branch advances the **MLOps Machine Maintenance** project by introducing the **`training_pipeline.py`** module inside the `pipeline/` directory.
It represents the **third executable workflow stage** of the project — combining **data preprocessing** and **model training** into a single, fully automated pipeline.

The training pipeline enables **end-to-end execution** of the machine learning workflow: from raw sensor data ingestion to model evaluation and persistence — all within one streamlined script.

## 🧩 **Overview**

The `training_pipeline.py` file orchestrates the project’s two key stages:

1️⃣ **Data Processing** — loads raw data, performs cleaning, encoding, scaling, and saves train/test splits.
2️⃣ **Model Training** — loads processed data, trains a Logistic Regression model, evaluates it, and saves the trained model to disk.

Both stages are powered by the core modules in `src/`:

* `data_processing.py`
* `model_training.py`
* `logger.py`
* `custom_exception.py`

This structure ensures that the workflow remains **reproducible**, **traceable**, and ready for **CI/CD integration**.

## 🔧 **Core Responsibilities**

| Stage | Operation              | Description                                                                                                          |
| ----: | ---------------------- | -------------------------------------------------------------------------------------------------------------------- |
|   1️⃣ | **Data Preprocessing** | Loads `data.csv`, cleans data, encodes categorical columns, standardises features, and saves processed artefacts.    |
|   2️⃣ | **Model Training**     | Loads processed data, trains a Logistic Regression model, saves it as `model.pkl`, and logs key performance metrics. |

## 🗂️ **Updated Project Structure**

```text
mlops_machine_maintenance/
├── .venv/                           # 🧩 Local virtual environment (created by uv)
├── artifacts/
│   ├── raw/
│   │   └── data.csv                 # ⚙️ Raw machine sensor dataset
│   ├── processed/                   # 💾 Processed data artefacts (train/test splits, scaler)
│   │   ├── X_train.pkl
│   │   ├── X_test.pkl
│   │   ├── y_train.pkl
│   │   ├── y_test.pkl
│   │   └── scaler.pkl
│   └── models/                      # 🧠 Trained model artefacts
│       └── model.pkl
├── pipeline/                        # ⚙️ Workflow orchestration layer
│   └── training_pipeline.py          # 🚀 End-to-end pipeline (data processing → model training)
├── src/
│   ├── __init__.py
│   ├── custom_exception.py          # Unified and detailed exception handling
│   ├── logger.py                    # Centralised logging configuration
│   ├── data_processing.py           # 🧩 Data preprocessing, scaling & splitting
│   └── model_training.py            # ⚙️ Model training, evaluation, and persistence
├── static/                          # 📊 Visual or diagnostic assets
├── templates/                       # 🧩 Placeholder for web/API templates
├── .gitignore                       # 🚫 Git ignore rules
├── .python-version                  # 🐍 Python version pin
├── pyproject.toml                   # ⚙️ Project metadata and uv configuration
├── requirements.txt                 # 📦 Python dependencies
├── setup.py                         # 🔧 Editable install support
└── uv.lock                          # 🔒 Locked dependency versions
```

## ⚙️ **How to Run the Training Pipeline**

After ensuring your raw dataset is available at `artifacts/raw/data.csv`, run the entire workflow with a single command:

```bash
python pipeline/training_pipeline.py
```

### ✅ **Expected Successful Output**

```console
2025-11-08 14:30:51,105 - INFO - Data processing initialised.
2025-11-08 14:30:51,432 - INFO - Basic data preprocessing completed.
2025-11-08 14:30:51,879 - INFO - Train/test splits and scaler saved successfully.
2025-11-08 14:30:52,210 - INFO - Model training initialised.
2025-11-08 14:30:52,622 - INFO - Model trained and saved successfully.
2025-11-08 14:30:53,002 - INFO - Accuracy : 0.85 ; Precision : 0.84 ; Recall : 0.85 ; F1 : 0.84
2025-11-08 14:30:53,145 - INFO - End-to-end training pipeline executed successfully.
```

This confirms that:

* The preprocessing and model training stages were executed sequentially.
* Artefacts were successfully written to `artifacts/processed/` and `artifacts/models/`.
* Evaluation metrics were logged for performance tracking.

## 🧠 **Implementation Highlights**

* **End-to-End Automation**
  Runs both preprocessing and model training in one script, simplifying experimentation and integration with CI/CD tools.

* **Integrated Logging** via `src/logger.py`
  Captures timestamped logs for every major step, creating a full audit trail for debugging and reproducibility.

* **Unified Error Handling** via `src/custom_exception.py`
  Standardises error messages and traceback details for clear, contextual debugging.

* **Production-Ready Architecture**
  The pipeline structure mirrors real-world MLOps patterns — modular, version-controlled, and scalable for future extensions.

## 🧩 **Integration Guidelines**

| File                            | Purpose                                                           |
| ------------------------------- | ----------------------------------------------------------------- |
| `pipeline/training_pipeline.py` | Orchestrates the full ML workflow from preprocessing to training. |
| `src/data_processing.py`        | Handles data cleaning, encoding, scaling, and persistence.        |
| `src/model_training.py`         | Performs model training, saving, and evaluation.                  |
| `src/logger.py`                 | Centralises logging across the pipeline.                          |
| `src/custom_exception.py`       | Provides structured, traceable error handling.                    |

## ✅ **In Summary**

This stage transforms the **MLOps Machine Maintenance** project into a **complete, end-to-end machine learning workflow**.
With a single command, the `training_pipeline.py` script orchestrates data preprocessing, model training, and evaluation — producing reproducible artefacts and detailed logs.

It lays the groundwork for **CI/CD automation**, **Kubeflow pipeline integration**, and **scalable model retraining workflows** in future stages of the project.
