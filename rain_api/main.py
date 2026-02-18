from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
import pickle
import numpy as np
import os
import logging

logging.basicConfig(level=logging.INFO)

# Create FastAPI instance
app = FastAPI(
    title="Rain Prediction API",
    version="1.0.0",
    description="ML API for predicting whether it will rain tomorrow."
)

model = None
threshold = None


# Get directory where main.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "rain_model.pkl")

# Load model and threshold once at startup
@app.on_event("startup")
def load_model():
    global model, threshold

    with open(model_path, "rb") as f:
        package = pickle.load(f)

    model = package["model"]
    threshold = package["threshold"]

EXPECTED_FEATURES = 21

# Define expected input structure
class RainInput(BaseModel):
    features: list[float] = Field(..., description="List of 21 weather features")

    @field_validator("features")
    def validate_length(cls, v):
        if len(v) != EXPECTED_FEATURES:
            raise ValueError(f"Exactly {EXPECTED_FEATURES} features required")
        return v
    
class RainOutput(BaseModel):
    probability: float
    prediction: int
    threshold_used: float


# Health check route
@app.get("/")
def home():
    return {"message": "Rain Prediction API is running"}

# Prediction route
@app.post("/predict", response_model=RainOutput)
def predict(data: RainInput):
    X = np.array(data.features).reshape(1, -1)
    
    try:

        probs = model.predict_proba(X)[:, 1][0]
        prediction = int(probs >= threshold)
        logging.info(f"Prediction made. Probability={probs}")


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {
        "probability": round(float(probs), 4),
        "prediction": prediction,
        "threshold_used": threshold
    }