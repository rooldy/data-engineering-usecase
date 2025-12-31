#!/bin/bash
# reorganize.sh

echo "🔄 Restructuring project..."

# 1. Déplacer src/ à la racine
if [ -d "airflow/src" ]; then
    echo "Moving src/ to root..."
    mv airflow/src ./src
fi

# 2. Nettoyer le dossier dags/ dupliqué à la racine
if [ -d "dags" ] && [ -d "airflow/dags" ]; then
    echo "Removing duplicate dags/ folder..."
    rm -rf dags
fi

# 3. Copier orchestration dans airflow/dags pour import facile
echo "Copying orchestration to dags..."
cp -r src/orchestration airflow/dags/

# 4. Mettre à jour docker-compose.yaml pour monter src/
echo "✅ Structure reorganized!"
echo ""
echo "Next steps:"
echo "1. Update docker-compose.yaml volumes to include src/"
echo "2. Restart Airflow containers"
