from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from typing import Dict
import pickle
import numpy as np
import os
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Rain Prediction API",
    version="1.0.0",
    description="ML API for predicting whether it will rain tomorrow."
)

# Global variables
model = None
threshold = None
feature_names = None

# Path to model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "rain_model_3.pkl")


# Load model at startup
@app.on_event("startup")
def load_model():
    global model, threshold, feature_names

    with open(model_path, "rb") as f:
        package = pickle.load(f)

    model = package["model"]
    threshold = package["threshold"]
    feature_names = package["feature_names"]

    logging.info("Model loaded successfully.")


# -----------------------------
# Request Schema
# -----------------------------
class RainInput(BaseModel):
    features: Dict[str, float]

    @field_validator("features")
    def validate_features(cls, v):
        if not isinstance(v, dict):
            raise ValueError("Features must be a dictionary")

        if len(v) != 21:
            raise ValueError("Exactly 21 features required")

        return v


# -----------------------------
# Response Schema
# -----------------------------
class RainOutput(BaseModel):
    probability: float
    prediction: int
    threshold_used: float


# -----------------------------
# Health Route
# -----------------------------
@app.get("/")
def home():
    return {"message": "Rain Prediction API is running"}


# -----------------------------
# Prediction Route
# -----------------------------
@app.post("/predict", response_model=RainOutput)
def predict(data: RainInput):

    if model is None or feature_names is None:
        raise HTTPException(status_code=500, detail="Model not loaded properly")

    # Check missing features
    missing = set(feature_names) - set(data.features.keys())
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing features: {list(missing)}"
        )

    # Reorder features according to training order
    try:
        X = np.array(
            [data.features[name] for name in feature_names]
        ).reshape(1, -1)

        probs = model.predict_proba(X)[0][1]
        prediction = int(probs >= threshold)

        logging.info(f"Prediction made. Probability={probs}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return RainOutput(
        probability=round(float(probs), 4),
        prediction=prediction,
        threshold_used=threshold
    )