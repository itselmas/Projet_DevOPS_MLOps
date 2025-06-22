import os
import time
import subprocess

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

print("[wait_for_model] Attente du modèle MLflow...")
model_path = None
while True:
    model_path = get_latest_model_path()
    if model_path:
        print(f"[wait_for_model] Modèle trouvé: {model_path}")
        break
    time.sleep(2)

# Lancer l'API FastAPI
subprocess.run(["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]) 