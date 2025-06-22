

## Comment démarrer

Pour lancer l'ensemble du pipeline (préparation des données, entraînement et déploiement de l'API), exécutez simplement le script d'orchestration adapté à votre système d'exploitation.

**Sous Windows :**
```bash
.\orchestrate.bat
```

**Sous Linux ou macOS :**
```bash
chmod +x orchestrate.sh
./orchestrate.sh
```
Une fois le script terminé, l'API de prédiction sera accessible à l'adresse [http://localhost:8000](http://localhost:8000).

## Tester l'API de prédiction

Vous pouvez tester l'API de deux manières :

1.  **Avec l'interface Swagger (recommandé) :**
    *   Rendez-vous sur [http://localhost:8000/docs](http://localhost:8000/docs).
    *   Dépliez la section `POST /predict`, cliquez sur `Try it out` et remplissez les champs avec des données d'exemple.

2.  **Avec `curl` (en ligne de commande) :**
    ```bash
    curl -X POST "http://localhost:8000/predict" \
    -H "Content-Type: application/json" \
    -d '{
      "median_income": 8.3, "housing_median_age": 41, "rooms_per_household": 7,
      "bedrooms_per_room": 0.15, "population_per_household": 2.5,
      "latitude": 37.8, "longitude": -122.2
    }'
    ```

## Détails du Pipeline MLOps

Le pipeline est orchestré par Docker Compose et se déroule en 3 étapes séquentielles :

1.  **`prepare_data`**
    *   Ce service lance le script `prepare_data.py`.
    *   Il nettoie le jeu de données brut (`data/housing_raw.csv`) et crée de nouvelles caractéristiques (features).
    *   Le résultat est sauvegardé dans `data/housing_clean.csv`.

2.  **`train`**
    *   Ce service exécute le script `training/train.py`.
    *   Il entraîne un modèle de régression linéaire sur les données nettoyées.
    *   Les métriques, paramètres et le modèle sont tracés et sauvegardés via **MLflow** dans le dossier `mlruns`.

3.  **`api`**
    *   Ce service déploie une API REST avec FastAPI.
    *   Au démarrage, il attend que le modèle soit disponible, puis charge automatiquement la dernière version du modèle depuis les artifacts MLflow.
    *   Il expose un endpoint `/predict` pour effectuer des prédictions.

## Structure du projet

```
.
├── api/                    # Contient le code de l'API FastAPI
│   ├── main.py             # Logique de l'API et endpoint /predict
│   └── wait_for_model.py   # Script pour attendre la création du modèle
├── data/                   # Contient les données
│   ├── housing_raw.csv     # Données brutes
│   └── ...
├── training/               # Contient le script d'entraînement
│   └── train.py
├── .gitignore              # Fichiers et dossiers à ignorer par Git
├── docker-compose.yml      # Orchestration des services Docker
├── Dockerfile              # Dockerfile pour l'entraînement/préparation
├── Dockerfile.api          # Dockerfile dédié à l'API
├── orchestrate.bat         # Script d'orchestration pour Windows
├── orchestrate.sh          # Script d'orchestration pour Linux/macOS
└── requirements.txt        # Dépendances Python
```

## API de Prédiction

Cette API REST permet de faire des prédictions à partir d'un modèle MLflow.

## Endpoints

### `POST /predict`
- **Description** : Effectue une prédiction à partir des features envoyées.
- **Body (JSON)** :
  ```json
  {
    "feature1": 1.23,
    "feature2": 4.56
    // ...
  }
  ```
- **Réponse (JSON)** :
  ```json
  {
    "prediction": 0.987
  }
  ```

## Lancement de l'API

1. Construire l'image Docker :
   ```sh
   docker build -t api-mlflow .
   ```
2. Lancer le conteneur :
   ```sh
   docker run -p 8000:8000 -e MLFLOW_MODEL_PATH=mlruns/0/<run_id>/artifacts/model api-mlflow
   ```

## Variables d'environnement
- `MLFLOW_MODEL_PATH` : chemin du modèle MLflow à charger.

## Pipeline complet
Un script d'automatisation permet de lancer toutes les étapes dans l'ordre : préparation des données, entraînement, puis lancement de l'API. 

## Utilisation du pipeline complet (local)

Pour automatiser la préparation des données, l'entraînement et le lancement de l'API :

- **Sous Windows** :
  ```bat
  run_all.bat
  ```
- **Sous Linux/Mac** :
  ```sh
  chmod +x run_all.sh
  ./run_all.sh
  ```

L'API sera accessible sur http://localhost:8000

## Lancement manuel de l'API (hors Docker)

Après avoir préparé les données et entraîné le modèle, lancez simplement :
```sh
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

## Lancer l'API de prédiction dockerisée (auto-détection du dernier modèle)

L'API FastAPI détecte automatiquement le dernier modèle MLflow loggé dans `mlruns/0/`.

Pour builder et lancer l'API FastAPI dans un conteneur dédié :

```sh
docker-compose up --build
```

L'API sera accessible sur http://localhost:8000

Vous n'avez plus besoin de modifier le run_id à la main dans le docker-compose ou les variables d'environnement. 

## Orchestration complète du pipeline (étape par étape)

Pour garantir que chaque étape se lance strictement après la fin de la précédente, utilisez les scripts d'orchestration :

- **Sous Linux/Mac** :
  ```sh
  chmod +x orchestrate.sh
  ./orchestrate.sh
  ```
- **Sous Windows** :
  ```bat
  orchestrate.bat
  ```

Chaque étape (préparation, entraînement, API) sera lancée dans l'ordre, et l'API sera accessible sur http://localhost:8000 