# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI(title="Demo Iris API")

# ⚠️ Chemin du modèle
MODEL_PATH = os.getenv("MODEL_PATH", "model.pkl")
model = joblib.load(MODEL_PATH)

# Schéma d'entrée : 4 features de l’iris
class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/")
def root():
    return {"status": "API OK 🎉"}

@app.post("/predict")
def predict(data: IrisFeatures):
    # 1) transforme en tableau numpy
    X = np.array([[data.sepal_length, data.sepal_width,data.petal_length, data.petal_width]])
    # 2) prédiction
    pred = int(model.predict(X)[0])
    # 3) réponse
    return {"class": pred}
