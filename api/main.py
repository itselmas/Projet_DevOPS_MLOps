from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.pyfunc
import os
import pandas as pd

app = FastAPI(title="API de Prédiction", description="API REST pour la prédiction via un modèle MLflow")

def get_latest_model_path(mlruns_path="mlruns"):
    try:
        experiments = [d for d in os.listdir(mlruns_path) if os.path.isdir(os.path.join(mlruns_path, d)) and d.isalnum()]
        if not experiments:
            return None

        latest_model_path = None
        latest_mtime = 0

        for exp_id in experiments:
            models_path = os.path.join(mlruns_path, exp_id, "models")
            if not os.path.exists(models_path):
                continue

            model_versions = [d for d in os.listdir(models_path) if os.path.isdir(os.path.join(models_path, d))]
            for model_version in model_versions:
                artifacts_path = os.path.join(models_path, model_version, "artifacts")
                if os.path.exists(artifacts_path):
                    mtime = os.path.getmtime(artifacts_path)
                    if mtime > latest_mtime:
                        latest_mtime = mtime
                        latest_model_path = artifacts_path
        
        return latest_model_path

    except Exception as e:
        print(f"Erreur lors de la recherche du dernier modèle: {e}")
        return None

# Chargement du modèle MLflow au démarrage
model = None
try:
    MLFLOW_MODEL_PATH = get_latest_model_path()
    if MLFLOW_MODEL_PATH:
        print(f"Chargement du modèle depuis: {MLFLOW_MODEL_PATH}")
        model = mlflow.pyfunc.load_model(MLFLOW_MODEL_PATH)
    else:
        print("Aucun modèle MLflow trouvé.")
except Exception as e:
    print(f"Erreur lors du chargement du modèle MLflow: {e}")

class PredictionRequest(BaseModel):
    # Features issues de prepare_data.py et train.py
    median_income: float
    housing_median_age: float
    rooms_per_household: float
    bedrooms_per_room: float
    population_per_household: float
    latitude: float
    longitude: float

@app.post("/predict")
def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Modèle non chargé")
    try:
        # Conversion en DataFrame pour compatibilité avec le modèle
        data = pd.DataFrame([request.dict()])
        prediction = model.predict(data)
        return {"prediction": float(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 