## Étape 3 — Architecture Technique Cible

### 🎯 Objectif de l’étape
Décrire précisément **l’architecture technique** de ton use case data engineering : les composants utilisés, les flux entre chaque couche, et la logique globale du pipeline (Ingestion → Stockage → Traitement → Transformation → Restitution).

---

## 🏗️ Architecture Technique Cible

### 1. **Sources de données**
- **ERP pharmaceutique** (données transactionnelles : ventes, stocks, livraisons)
- **Système de capteurs IoT** (consommation énergétique, mesure en temps réel)
- **Fichiers CSV / JSON** déposés dans un bucket S3 ou un dossier partagé
- **Base PostgreSQL** interne (référentiels, produits, entités)
- **API externes** pour récupérer des mises à jour réglementaires

---

### 2. **Ingestion des données**
- **AWS S3** comme point d’atterrissage (_landing zone_)
- **AWS Glue Jobs / Python / PySpark**
  - ingestion batch depuis S3
  - ingestion JDBC depuis PostgreSQL
  - ingestion streaming depuis capteurs IoT via Amazon Kinesis
- **Airflow** pour orchestrer les DAG :
  - `dag_ingest_erp`
  - `dag_ingest_iot`
  - `dag_ingest_ref_data`

---

### 3. **Zone de stockage (Data Lake)**
Organisation en 3 zones standard :
- **Bronze** : données brutes (raw)
- **Silver** : données nettoyées et structurées
- **Gold** : données business prêtes pour l’analyse et la BI

Stockage principal :
- **S3 Data Lake** avec partitionnement :
  - `/bronze/source=erp/year=2025/month=12/day=01/`
  - `/silver/domain=pharma/table=ventes/`
  - `/gold/domain=energy/model=prediction/`

Format utilisé :
- **Parquet** (optimisé pour lecture analytique)
- **Delta Lake** (si need versioning & ACID)

---

### 4. **Traitement et Transformation**
- **AWS Glue / PySpark / Spark Scala**
  - nettoyages (schemas, types, formats)
  - jointures entre référentiels (produits, zones, machines)
  - enrichissement par les données de capteurs
  - détection d’anomalies (outliers)
  - calcul des KPI métiers
- **Snowflake** (si inclusion prévue) :
  - loading via Snowpipe
  - transformation SQL (ELT)
  - création de vues métiers

---

### 5. **Modélisation**
- **Modèle en étoile** (_Star Schema_) :
  - Tables de faits :
    - `fact_ventes`
    - `fact_consommation_energie`
    - `fact_production`
  - Tables de dimensions :
    - `dim_produit`
    - `dim_machine`
    - `dim_temps`
    - `dim_site`
- Business rules appliquées :
  - calcul des marges
  - classification des anomalies
  - normalisation énergétique par production

---

### 6. **Orchestration & automatisation**
- **Apache Airflow**
  - planification quotidienne
  - gestion des dépendances
  - intégration GitHub + CI/CD
  - alertes sur erreur
- Pipelines typiques :
  - `pipeline_ingestion`
  - `pipeline_transformation`
  - `pipeline_qualite`
  - `pipeline_load_bi`

---

### 7. **Restitution & Analyse**
- **Power BI / Tableau**
  - tableaux de bord pharmaceutiques :
    - taux de rupture
    - performance logistique
  - dashboards énergie :
    - consommation en temps réel
    - anomalies machines
- Exposition des données via :
  - API internes
  - Vues Snowflake / Postgres pour la BI

---

### 8. **Sécurité & Gouvernance**
- **IAM Fine-grained access**
- **Chiffrement S3 KMS**
- **Gestion des logs CloudTrail**
- **Data quality : Great Expectations**
- **Catalogage & metadonnées : AWS Glue Catalog**
- **Conformité : GDPR + normes pharmaceutiques**

---

### 🔥 Résultat attendu
Une architecture complète, scalable et sécurisée permettant :
- d’ingérer plusieurs types de données
- de les transformer en tables analytiques
- de produire un reporting fiable
- de supporter un cas d’usage pharmaceutique + énergie

