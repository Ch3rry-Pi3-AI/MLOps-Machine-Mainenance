from __future__ import annotations

import json
import os
from datetime import datetime

import joblib
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

# ---------------------------------------------------------------------
# Paths to artefacts
# ---------------------------------------------------------------------
MODEL_PATH = "artifacts/models/model.pkl"
SCALER_PATH = "artifacts/processed/scaler.pkl"
MEANS_PATH = "artifacts/processed/feature_means.json"  # optional, if you save means at preprocessing

# ---------------------------------------------------------------------
# Load artefacts
# ---------------------------------------------------------------------
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# ---------------------------------------------------------------------
# Feature schema (order must match training)
# ---------------------------------------------------------------------
FEATURES = [
    "Operation_Mode",
    "Temperature_C",
    "Vibration_Hz",
    "Power_Consumption_kW",
    "Network_Latency_ms",
    "Packet_Loss_%",
    "Quality_Control_Defect_Rate_%",
    "Production_Speed_units_per_hr",
    "Predictive_Maintenance_Score",
    "Error_Rate_%",
    "Year",
    "Month",
    "Day",
    "Hour",
]

# ---------------------------------------------------------------------
# Label mapping (model outputs → human-readable class)
# Adjust if your training produced different indices
# ---------------------------------------------------------------------
LABELS = {
    0: "High",
    1: "Low",
    2: "Medium",
}

# ---------------------------------------------------------------------
# Operation mode encoding used during training
# If you persisted encoders, load them; otherwise fall back to this map.
# Note: Ensure this mapping matches the one seen in logs during preprocessing.
# Example seen previously: {'Idle': 0, 'Active': 1, 'Maintenance': 2}
# ---------------------------------------------------------------------
OPERATION_MODE_MAP = {
    "Idle": 0,
    "Active": 1,
    "Maintenance": 2,
}

OPERATION_MODE_CHOICES = list(OPERATION_MODE_MAP.keys())

# ---------------------------------------------------------------------
# Sensible default values
# If feature means were saved, use them; otherwise use these fallbacks.
# ---------------------------------------------------------------------
_now = datetime.now()
DEFAULTS_FALLBACK = {
    "Operation_Mode": "Active",              # UI value; mapped via OPERATION_MODE_MAP
    "Temperature_C": 65.0,                   # typical operating temperature
    "Vibration_Hz": 50.0,                    # nominal frequency
    "Power_Consumption_kW": 35.0,            # mid-load power
    "Network_Latency_ms": 15.0,              # LAN-ish latency
    "Packet_Loss_%": 0.5,
    "Quality_Control_Defect_Rate_%": 1.0,
    "Production_Speed_units_per_hr": 120.0,
    "Predictive_Maintenance_Score": 55.0,    # health score out of 100
    "Error_Rate_%": 0.8,
    "Year": _now.year,
    "Month": _now.month,
    "Day": _now.day,
    "Hour": min(_now.hour, 23),
}

def load_feature_means() -> dict:
    if os.path.exists(MEANS_PATH):
        try:
            with open(MEANS_PATH, "r", encoding="utf-8") as f:
                means = json.load(f)
            # Merge: keep UI-friendly defaults for Operation_Mode & date parts
            merged = DEFAULTS_FALLBACK.copy()
            for k, v in means.items():
                if k in merged and isinstance(v, (int, float)):
                    merged[k] = v
            return merged
        except Exception:
            return DEFAULTS_FALLBACK
    return DEFAULTS_FALLBACK

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    form_values = load_feature_means()

    if request.method == "POST":
        try:
            # Build input vector in FEATURE order
            values = []
            for feat in FEATURES:
                if feat == "Operation_Mode":
                    mode_label = request.form.get("Operation_Mode", OPERATION_MODE_CHOICES[0])
                    mode_code = OPERATION_MODE_MAP.get(mode_label)
                    if mode_code is None:
                        raise ValueError(f"Unknown Operation_Mode '{mode_label}'.")
                    values.append(float(mode_code))
                    form_values["Operation_Mode"] = mode_label
                else:
                    raw_val = request.form.get(feat, str(DEFAULTS_FALLBACK.get(feat, 0.0)))
                    val = float(raw_val)
                    values.append(val)
                    form_values[feat] = val

            input_array = np.array(values, dtype=float).reshape(1, -1)
            scaled_array = scaler.transform(input_array)
            pred_idx = int(model.predict(scaled_array)[0])
            prediction = LABELS.get(pred_idx, f"Unknown ({pred_idx})")
        except Exception as e:
            prediction = f"Error: {e}"

    return render_template(
        "index.html",
        prediction=prediction,
        features=FEATURES,
        defaults=form_values,
        op_modes=OPERATION_MODE_CHOICES,
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
