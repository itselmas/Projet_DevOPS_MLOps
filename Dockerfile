# Dockerfile pour l'entraînement
FROM python:3.10-slim

WORKDIR /app

# Installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier les fichiers Python
COPY prepare_data.py .
COPY train.py .
COPY verify_data.py .

# Copier les données brutes
COPY data/ ./data/

# Lancer la préparation + entraînement automatiquement
CMD python prepare_data.py && python train.py
