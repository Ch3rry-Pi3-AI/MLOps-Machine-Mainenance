"""
training_pipeline.py
===============
Executes the full MLOps Machine Maintenance workflow — from **data preprocessing**
to **model training and evaluation** — as a single orchestrated script.

Overview
--------
This script serves as an **end-to-end pipeline runner**, chaining together:
1) Data preprocessing using `DataProcessing`
2) Model training and evaluation using `ModelTraining`

It demonstrates how the two primary workflow stages can be integrated seamlessly
within the same execution flow.

Execution
---------
Run the script directly from the project root:

    python run_pipeline.py

Expected Output
---------------
The console (and `logs/`) will include messages for:
- Data loading, preprocessing, encoding, and scaling
- Train/test split creation and persistence
- Model training, saving, and evaluation metrics (Accuracy, Precision, Recall, F1)
"""

# -------------------------------------------------------------------
# Internal imports
# -------------------------------------------------------------------
from src.data_processing import DataProcessing
from src.model_training import ModelTraining


# -------------------------------------------------------------------
# Main pipeline orchestration
# -------------------------------------------------------------------
if __name__ == "__main__":
    # ----------------------------------------------------------------
    # Stage 1: Data Preprocessing
    # ----------------------------------------------------------------
    processor = DataProcessing(
        input_path="artifacts/raw/data.csv",
        output_path="artifacts/processed"
    )
    processor.run()

    # ----------------------------------------------------------------
    # Stage 2: Model Training & Evaluation
    # ----------------------------------------------------------------
    trainer = ModelTraining(
        processed_data_path="artifacts/processed/",
        model_output_path="artifacts/models/"
    )
    trainer.run()
