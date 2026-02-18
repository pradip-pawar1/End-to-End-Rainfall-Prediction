from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
import os

# Create FastAPI instance
app = FastAPI(title="Rain Prediction API")

# Get directory where main.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "rain_model.pkl")

# Load model and threshold once at startup
with open(model_path, "rb") as f:
    package = pickle.load(f)

model = package["model"]
threshold = package["threshold"]


# Define expected input structure
class RainInput(BaseModel):
    features: list[float]


# Health check route
@app.get("/")
def home():
    return {"message": "Rain Prediction API is running"}


# Prediction route
@app.post("/predict")
def predict(data: RainInput):
    try:
        X = np.array(data.features).reshape(1, -1)

        probs = model.predict_proba(X)[:, 1]
        prediction = int(probs >= threshold)

        return {
            "probability": float(probs),
            "prediction": prediction,
            "threshold_used": threshold
        }

    except Exception as e:
        return {"error": str(e)}
