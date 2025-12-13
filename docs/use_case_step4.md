## Étape 4 — Pipeline de Données (Conception + Fonctionnement Technique)

### 🎯 Objectif de l’étape
Décrire précisément **le fonctionnement complet du pipeline de données**, depuis l’arrivée des données brutes jusqu’à la livraison des données business prêtes à l’usage (BI, reporting, analyses).  
Cette étape explique **comment les pipelines ETL/ELT sont conçus, orchestrés, automatisisés et contrôlés**.

---

# 🛠️ Pipeline de Données — Déroulement Technique

## 1. **Ingestion des données (Extract)**

### ✦ Sources ingérées
- ERP pharmaceutique (ventes, stocks, livraisons)
- PostgreSQL (référentiels produits / sites)
- IoT via Kinesis (mesures énergétiques en temps réel)
- Fichiers CSV/JSON déposés sur S3
- API externes (données réglementaires)

### ✦ Mécanismes d’ingestion
- **Airflow** déclenche des DAG d’ingestion :
  - `dag_ingest_erp`
  - `dag_ingest_iot`
  - `dag_ingest_ref_data`
- **Glue Jobs / PySpark** pour effectuer :
  - Extraction via connecteur JDBC
  - Lecture fichiers S3
  - Traitement streaming IoT

### ✦ Stockage en zone Bronze
- Tous les fichiers sont stockés **tels quels** (raw)
- Format conservé : CSV, JSON ou Parquet
- Naming convention strict :
  - `/bronze/source=erp/date=2025-01-15/ventes_raw.json`
  - `/bronze/source=iot/device_id=capteur_42/2025/05/10/…`

---

## 2. **Nettoyage + Normalisation (Transform — Silver)**

### ✦ Nettoyages effectués automatiquement
- Correction des types (dates, float, int)
- Gestion des valeurs manquantes
- Normalisation des colonnes (noms, formats)
- Suppression des doublons
- Gestion des schémas évolutifs (Schema Evolution)

### ✦ Transformations techniques
Réalisées dans **PySpark / Glue** :
- Standardisation du schéma "ventes"
- Jointure avec référentiel produits
- Conversion en **Parquet** ou **Delta Lake**
- Partitionnement par métier + date

### ✦ Stockage en Silver
- Données propres, structurées et cohérentes
- Exemple :
  - `/silver/pharma/table=ventes/year=2025/month=01/`
  - `/silver/energy/table=mesures_iot/`

---

## 3. **Enrichissement + Modélisation (Transform — Gold)**

### ✦ Règles métier appliquées
- Calcul des KPI pharmaceutiques :
  - ruptures de stock
  - taux de service
  - délai de livraison
- Calcul des KPI énergétiques :
  - consommation moyenne
  - détection d’anomalies (écarts standard)
  - efficacité énergétique par machine
- Ajout des dimensions :
  - produit
  - site
  - machine
  - temps

### ✦ Modèles de données produits
- **Faits (fact tables)**
  - `fact_ventes`
  - `fact_energie`
  - `fact_production`
- **Dimensions**
  - `dim_produit`
  - `dim_machine`
  - `dim_site`
  - `dim_temps`

### ✦ Stockage en Gold
- Tables business optimisées pour la BI
- Format Parquet ou Delta (ACID)
- Exemple :
  - `/gold/pharma/fact_ventes/`
  - `/gold/energy/fact_energie/`

---

## 4. **Charge dans l’entrepôt (Load)**

### ✦ Snowflake (si utilisé)
- **Snowpipe** charge automatique des fichiers Gold
- Task SQL pour transformations additionnelles
- Vues sécurisées pour le reporting

### ✦ PostgreSQL (si BI interne)
- Chargement par Airflow + opérateurs PostgreSQL
- Création de vues matérialisées

---

## 5. **Orchestration complète via Airflow**

### ✦ DAG principaux
- `dag_ingestion_data`
- `dag_cleaning_silver`
- `dag_modeling_gold`
- `dag_quality_checks`
- `dag_load_bi`

### ✦ Fonctionnement
- Dépendances définies :
  - Bronze → Silver → Gold → BI
- Gestion des erreurs :
  - alertes email Slack
  - retry automatique
- Logs centralisés

---

## 6. **Contrôles qualité & Gouvernance**

### ✦ Qualité (DQ)
- Tests Great Expectations :
  - Validité (schémas)
  - Unicité des identifiants
  - Contraintes métiers (ex : stock ≥ 0)

### ✦ Métadonnées
- AWS Glue Data Catalog :
  - schémas
  - lineage
  - versioning

### ✦ Sécurité
- IAM Policies
- Encryption S3 (KMS)
- Restriction par rôle (RBAC)

---

# 🚀 Résultat attendu
Un pipeline complet, robuste et industrialisé, capable de :
- gérer plusieurs sources hétérogènes
- automatiser toutes les étapes
- produire des tables analytiques fiables
- supporter un reporting pharmaceutique + énergétique
- garantir qualité, sécurité et gouvernance.

