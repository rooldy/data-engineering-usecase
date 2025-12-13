# Étape 5 — Architecture Airflow + Design des DAGs

### 🎯 Objectif de l’étape
Documenter **l’architecture Airflow**, la logique des **DAGs**, les dépendances, les opérateurs utilisés et les bonnes pratiques d’orchestration.  
Cette section montre ta capacité à **industrialiser un pipeline de données** avec monitoring, gestion des erreurs et automatisation complète.

---

# 1. **Architecture Airflow (Vue globale)**

Le projet repose sur une orchestration complète via **Apache Airflow**, permettant :

- l’automatisation de l’ingestion → transformation → modélisation → chargement  
- la surveillance des jobs  
- l’observabilité (logs, retries, SLA)  
- le versioning via Git  
- la modularité par DAGs distincts  

### 🧱 **Composants Airflow utilisés**
- **Scheduler** → planification et envoi des tâches au Worker  
- **Webserver** → interface de monitoring  
- **Worker / Celery / Kubernetes Executor** (selon setup)  
- **Metadata DB** → suivi des DAG Runs + Task Instances  
- **Connections & Variables** → gestion des secrets et paramètres  

---

# 2. **Structure des DAGs dans le projet**

```
airflow/
 ├── dags/
 │    ├── dag_ingestion.py
 │    ├── dag_cleaning_silver.py
 │    ├── dag_modeling_gold.py
 │    ├── dag_load_to_snowflake.py
 │    ├── dag_quality_checks.py
 │    └── dag_master_pipeline.py
 ├── plugins/
 │    ├── operators/
 │    └── hooks/
 └── configs/
```

---

# 3. **DAG 1 — Ingestion (Bronze)**

### 📌 Nom : `dag_ingestion.py`

### 🎯 Rôle  
Ingestion automatique des données provenant de :
- PostgreSQL  
- API externes  
- IoT / Kinesis  
- Fichiers CSV/JSON sur S3  

### 🧩 Tasks typiques  
- `extract_postgres`
- `extract_api_data`
- `extract_iot_stream`
- `upload_to_bronze`

### 🔧 Opérateurs utilisés  
- `PythonOperator`  
- `S3UploadOperator`  
- `PostgresHook`  
- `SimpleHttpOperator`

### 🔗 Dépendances

```
extract_postgres → upload_to_bronze
extract_api_data → upload_to_bronze
extract_iot_stream → upload_to_bronze
```

---

# 4. **DAG 2 — Nettoyage & Normalisation (Silver)**

### 📌 Nom : `dag_cleaning_silver.py`

### 🎯 Rôle  
Normalisation + qualité + validation.

### ✨ Exemples  
- Conversion dates  
- Correction typages  
- Suppression doublons  
- Standardisation schémas  

### 🔧 Opérateurs/techno  
- `GlueJobOperator`  
- `SparkSubmitOperator`  
- `PythonOperator`

### 🔗 Flux d’exécution

```
read_bronze_data
    → apply_cleaning_rules
    → validate_schema
    → write_silver_data
```

---

# 5. **DAG 3 — Modélisation (Gold)**

### 📌 Nom : `dag_modeling_gold.py`

### 🎯 Rôle  
Créer les tables métier : fact & dimension.

### 🧩 Tasks  
- `build_dim_tables`
- `build_fact_ventes`
- `build_fact_energie`
- `merge_gold_tables`

### 🔧 Opérateurs  
- `SparkSubmitOperator`
- `PythonOperator`

### 🔗 Flux

```
build_dim_tables → build_fact_tables → merge_gold_tables
```

---

# 6. **DAG 4 — Chargement Snowflake**

### 📌 Nom : `dag_load_to_snowflake.py`

### 🎯 Rôle  
Charger les données Gold dans Snowflake (ou autre DWH).

### 📌 Tasks  
- `stage_upload_files`
- `run_copy_into_commands`
- `refresh_materialized_views`

### 🔧 Opérateurs  
- `SnowflakeOperator`
- `S3ToSnowflakeOperator`  
- `PythonOperator`  

---

# 7. **DAG 5 — Contrôles Qualité**

### 📌 Nom : `dag_quality_checks.py`

### 🎯 Rôle  
Assurer la qualité des données via automatisation.

### 🧩 Types de tests  
- Tests schémas  
- Unicité clé primaire  
- Valeurs nulles  
- Contraintes métier  
- Distribution (profiling)

### 🔧 Outils  
- Great Expectations (intégré à Airflow)
- PythonOperator

---

# 8. **DAG 6 — Master Pipeline**

### 📌 Nom : `dag_master_pipeline.py`

### 🎯 Rôle  
Coordonner l’ensemble des DAGs pour exécuter un pipeline complet.

### 🔗 Structure du DAG global

```
dag_ingestion
      ↓
dag_cleaning_silver
      ↓
dag_modeling_gold
      ↓
dag_quality_checks
      ↓
dag_load_to_snowflake
```

Avec gestion stricte :
- des dépendances
- des règles de retry
- des SLA par couche

---

# 9. **Gestion des erreurs, alertes & monitoring**

### 🚨 Alerting
- Email
- Slack Webhook
- Push monitoring (Grafana, Prometheus)

### 🔁 Retry policies
- retry = 3  
- backoff = True  
- retry_delay = 3 minutes

### 🕵️ Logs
- Logs stockés dans S3 / CloudWatch / Loki  
- Toutes les exécutions sont historisées

---

# 10. **Bonnes pratiques Airflow appliquées**

✔ Un DAG = une logique métier  
✔ Un DAG ne contient pas la logique de transformation (externalisation PySpark)  
✔ Tâches idempotentes  
✔ Dépendances explicites  
✔ Configuration via Variables Airflow  
✔ Secrets stockés dans AWS Secrets Manager  
✔ Tests unitaires pour les opérateurs personnalisés  
✔ Versioning Git obligatoire avant déploiement  

---

# 🚀 Résultat attendu

Une orchestration **hautement professionnelle**, montrant :
- une séparation claire des responsabilités  
- une industrialisation complète  
- une observabilité parfaite  
- une architecture Airflow robuste et scalable  

Cette étape montre ta capacité à piloter un pipeline **end-to-end**, digne d’un Data Engineer confirmé.

