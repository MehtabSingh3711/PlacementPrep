import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

X = np.array([
    [0.9, 275, 1.2, 60, 20],
    [1.1, 285, 1.5, 55, 18],
    [0.95, 290, 0.8, 65, 22],
    [4.2, 90, 0.2, 8, 4],
    [0.5, 450, 50, 15, 0],
    [0.3, 650, 0.1, 5, 2],
    [3.5, 120, 0.3, 10, 3],
    [0.15, 750, 0.05, 0, 1],
    [1.3, 270, 1.1, 50, 19],
    [0.85, 295, 1.6, 70, 21]
])
y = np.array([1, 1, 1, 0, 0, 0, 0, 0, 1, 1])

from sklearn.tree import DecisionTreeClassifier as dtc 
model = dtc()
model.fit(X, y)
# FastAPI app
app = FastAPI(title="Exoplanet Habitability API")

# Request model
class ExoplanetFeatures(BaseModel):
    distance_au: float
    temp_k: float
    pressure_atm: float
    water_pct: float
    oxygen_pct: float

# Prediction endpoint
@app.post("/predict")
def predict_habitability(features: ExoplanetFeatures):
    X_new = np.array([[
        features.distance_au,
        features.temp_k,
        features.pressure_atm,
        features.water_pct,
        features.oxygen_pct
    ]])
    prediction = int(model.predict(X_new)[0])
    result = "habitable" if prediction == 1 else "uninhabitable"
    
    return {
        "prediction": prediction,
        "result": result,
        "features": features.dict()
    }

# Health check
@app.get("/")
def root():
    return {"message": "Exoplanet Habitability API is running", "accuracy": float(model.score(X, y))}

