# **ÉTAPE 2 — Architecture cible du Use Case Data Engineering**

## 🎯 Objectif de l’étape  
Décrire clairement l’architecture technique mise en place pour ingérer, stocker, transformer et exposer les données.  
Cette section sert de référence pour comprendre comment les outils interagissent et comment les flux circulent.

---

# **2. Architecture cible**

## **2.1. Vue d’ensemble**

L’architecture du projet repose sur une chaîne Data Engineering moderne comprenant :

- **Amazon S3** pour le stockage (bronze, silver, gold)  
- **AWS Glue / PySpark** pour les transformations  
- **Apache Airflow** pour l’orchestration  
- **Snowflake** pour les traitements analytiques  
- **Outils BI** (Power BI / Tableau) pour la visualisation  

Elle suit un modèle **Lakehouse** structuré autour des zones :

| Zone   | Rôle |
|--------|------|
| **Bronze** | Données brutes |
| **Silver** | Données nettoyées et conformes |
| **Gold** | Données modélisées pour l’analyse |

---

## **2.2. Architecture détaillée (composants)**

### 🔹 **1. Sources**
- API REST  
- Fichiers CSV/JSON  
- Base de données type PostgreSQL

### 🔹 **2. Stockage — S3**
- `landing/` → données entrantes  
- `bronze/` → données ingérées  
- `silver/` → données normalisées  
- `gold/` → tables finalisées  

### 🔹 **3. Orchestration — Airflow**
DAGs principaux :
- `dag_ingestion.py`  
- `dag_transformation.py`  
- `dag_loading_snowflake.py`

### 🔹 **4. Traitement — Glue / PySpark**
- Standardisation des schémas  
- Nettoyage et validation  
- Règles métiers  
- Optimisation (parquet, partitionnement)

### 🔹 **5. Snowflake**
- Insertion batch  
- Création de tables métiers  
- Vues analytiques  
- Streams & Tasks (si CDC)

### 🔹 **6. Restitution**
- Power BI / Tableau  
- Connexion directe Snowflake  
- KPIs métiers et dashboards

---

## **2.3. Schéma Architecture**

      [ API / DB / CSV ]
               |
               v
     ┌────────────────────┐
     │    Landing S3      │
     └────────────────────┘
               |
         Airflow DAG
               |
               v
     ┌────────────────────┐
     │    Bronze S3       │
     └────────────────────┘
               |
         PySpark / Glue
               |
               v
     ┌────────────────────┐
     │     Silver S3      │
     └────────────────────┘
               |
         PySpark / ELT
               |
               v
     ┌────────────────────┐
     │      Snowflake     │
     └────────────────────┘
               |
             BI Tools


---

## **2.4. Bénéfices**

- Architecture modulaire  
- Séparation des zones de données  
- Observabilité avec Airflow + Snowflake  
- Facile à industrialiser (CI/CD, monitoring)

---

## **2.5. Rôle des couches**

| Couche | Fonction | Exemple |
|--------|----------|---------|
| **Bronze** | Données brutes | CSV déposés tels quels |
| **Silver** | Nettoyage / typage | Formats date, suppression doublons |
| **Gold** | Tables métiers | `sales_daily_metrics` |

