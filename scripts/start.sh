#!/bin/bash

echo "Démarrage de l'environnement Data Engineering"

cd docker || exit 1
docker-compose up --build -d

echo "🌐 Airflow UI : http://localhost:8080"
