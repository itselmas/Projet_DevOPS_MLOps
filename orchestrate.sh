#!/bin/bash
set -e

echo "[1/3] Préparation des données..."
docker compose run --rm prepare_data

echo "[2/3] Entraînement du modèle..."
docker compose run --rm train

echo "[3/3] Lancement de l'API..."
docker compose up api 