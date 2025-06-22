@echo off
REM [1/3] Préparation des données
call docker compose run --rm prepare_data

REM [2/3] Entraînement du modèle
call docker compose run --rm train

REM [3/3] Lancement de l'API
call docker compose up api 