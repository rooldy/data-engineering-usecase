#!/bin/bash

echo "Arrêt de l'environnement Data Engineering"

cd docker || exit 1
docker-compose down
