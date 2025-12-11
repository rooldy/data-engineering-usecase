# data-engineering-usecase

# 🏗️ E-Commerce Data Engineering Pipeline  
Pipeline complet de traitement des transactions d’un site e-commerce avec ingestion, transformation, stockage analytique et orchestration.

---

## 📌 1. Objectif du projet

Ce projet simule un cas réel d’entreprise :  
Une plateforme e-commerce souhaite suivre ses KPIs clés :

- CA journalier / hebdomadaire / mensuel  
- Nombre de transactions par catégorie produit  
- Taux de retour  
- Valeur moyenne du panier (AOV)  
- Top produits vendus  
- Activité par client / géographie  

Le but est de construire un **pipeline de données de bout en bout**, automatisé et industrialisé.

---

## 📦 2. Architecture du pipeline

Le pipeline repose sur trois couches principales :

### **1. Ingestion**
- Chargement de fichiers CSV/JSON dans une zone *raw*
- Nettoyage minimal
- Gestion du format et horodatage

### **2. Processing (PySpark)**
- Nettoyage avancé
- Détection d’anomalies
- Normalisation des colonnes
- Enrichissement des données
- Calcul des KPIs intermédiaires

### **3. Analytics**
- Création des datasets analytiques prêts pour reporting/dashboards
- Agrégations PySpark ou Pandas selon le cas

### **4. Orchestration (Airflow)**
- Un DAG unique qui automatise l’ensemble

---

## 🛠️ 3. Technologies utilisées

| Composant | Technologie |
|----------|-------------|
| Orchestration | Apache Airflow |
| Processing Big Data | PySpark |
| Data Exploration | Pandas / Notebooks |
| Conteneurisation | Docker |
| Tests | Pytest |
| CI/CD | GitHub Actions (à venir) |
| Stockage | Local filesystem (simule Data Lake) |

---

## 📁 4. Structure du projet

```
src/
│── ingestion/
│── processing/
│── analytics/
dags/
docker/
tests/
configs/
notebooks/
data/
```

---

## 🚀 5. Exécution du projet (en local)

### 1. Cloner le repo  
```bash
git clone https://github.com/rooldy/data-engineering-usecase.git
cd data-engineering-usecase
```

### 2. Installer les dépendances  
```bash
pip install -r requirements.txt
```

### 3. Lancer Airflow (Docker)  
```bash
docker-compose up --build
```

L’interface sera disponible sur :  
➡️ http://localhost:8080

---

## 🧪 6. Tests

```bash
pytest tests/
```

---

## 📌 7. TODO (feuille de route du projet)

- [ ] Ajouter l’image d’architecture complète  
- [ ] Écrire le DAG Airflow  
- [ ] Développer ingestion (CSV → raw)  
- [ ] Développer transformations PySpark  
- [ ] Développer analytics (KPIs)  
- [ ] Ajouter CI/CD GitHub Actions  
- [ ] Ajouter monitoring basique  
- [ ] Ajouter dashboard (Power BI ou Superset)

---

## 👤 Auteur  
**Rooldy — Data Engineer**

