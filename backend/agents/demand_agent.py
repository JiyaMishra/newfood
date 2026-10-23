# backend/agents/demand_agent.py
"""Demand Forecasting Agent
Loads the trained Random Forest model and predicts expected consumers.
"""
import os
import joblib
from pathlib import Path
from ..schemas import DemandRequest

MODEL_PATH = Path(__file__).resolve().parent.parent / "model.joblib"

def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Trained model not found at {}".format(MODEL_PATH))
    data = joblib.load(str(MODEL_PATH))
    return data["model"], data.get("version", "unknown")

def demand_forecast(req: DemandRequest):
    model, version = load_model()
    # Build feature vector matching training columns
    features = [
        req.attendance_estimate,
        req.exam_intensity,
        req.temperature_c,
        req.rainfall_mm,
        req.historical_demand_rate,
        # placeholder for liking_score, if not provided use 0.5
        getattr(req, "synthetic_liking_score", 0.5),
    ]
    # model expects 2D array
    pred = model.predict([features])[0]
    # round to nearest integer
    pred_int = int(round(pred))
    return pred_int, version
