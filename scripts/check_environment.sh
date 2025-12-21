#!/bin/bash

echo " Vérification de l'environnement Data Engineering"
echo "--------------------------------------------------"

# Vérifier que le conteneur PySpark est lancé
if ! docker ps | grep -q pyspark_local; then
  echo " Le conteneur pyspark_local n'est pas lancé"
  exit 1
fi

echo " Conteneur pyspark_local actif"

# Vérifier les données RAW
echo ""
echo "Vérification des données RAW :"
docker exec -it pyspark_local ls /app/data/raw || {
  echo " Dossier /app/data/raw introuvable"
  exit 1
}

# Vérifier Spark
echo ""
echo " Vérification Spark :"
docker exec -it pyspark_local spark-submit --version

echo ""
echo "Environnement prêt !"

