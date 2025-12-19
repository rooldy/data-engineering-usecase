"""
=========================================================
SCRIPT : generate_raw_data.py
OBJECTIF :
- Generer des donnees brutes (RAW) en CSV
- Simuler une plateforme e-commerce a grande echelle
- Volumetrie realiste (millions de lignes)
- Base pour pipelines Spark / Airflow / Snowflake

AUTEUR : Rooldy
=========================================================
"""

# =====================
# IMPORTS
# =====================
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,           # manipulation de colonnes
    lit,           # valeurs constantes
    rand,          # generation aleatoire
    concat,        # concatenation de colonnes
    current_date,  # date du jour
    expr           # expressions SQL
)

# =====================
# INITIALISATION SPARK
# =====================
# Creation de la SparkSession (point d'entree de Spark)
spark = (
    SparkSession.builder
    .appName("GenerateRawCSV")
    .getOrCreate()
)

# Reduction du nombre de partitions shuffle
# Important pour eviter trop de petits fichiers
spark.conf.set("spark.sql.shuffle.partitions", "200")

# Chemin racine des donnees RAW
BASE_PATH = "/app/data/raw"

# =====================
# PARAMETRES DE VOLUMETRIE
# =====================
# Ces valeurs permettent de simuler un vrai SI e-commerce
NB_CLIENTS = 1_000_000
NB_PRODUITS = 200_000
NB_COMMANDES = 3_000_000
NB_LIGNES_CMD = 8_000_000
NB_PANIERS = 1_500_000

# =========================================================
# ===================== CLIENTS ===========================
# =========================================================
# Table de reference clients (dimension)
clients = (
    spark.range(1, NB_CLIENTS + 1)            # Generation d'IDs sequentiels
    .withColumnRenamed("id", "client_id")     # Cle primaire
    .withColumn("nom", concat(lit("Client_"), col("client_id")))
    .withColumn("email", concat(lit("client"), col("client_id"), lit("@mail.com")))
    .withColumn("pays", lit("FR"))
    .withColumn("date_creation", current_date())
    .repartition(200)                         # Controle du nombre de fichiers
)

# Ecriture en CSV (RAW layer)
clients.write.mode("overwrite") \
    .option("header", "true") \
    .csv(f"{BASE_PATH}/clients")

# =========================================================
# ===================== PRODUITS ==========================
# =========================================================
# Table de reference produits
produits = (
    spark.range(1, NB_PRODUITS + 1)
    .withColumnRenamed("id", "produit_id")
    # Categorisation simple mais realiste
    .withColumn(
        "categorie",
        expr("""
            CASE
                WHEN produit_id % 3 = 0 THEN 'Tech'
                WHEN produit_id % 3 = 1 THEN 'Maison'
                ELSE 'Mode'
            END
        """)
    )
    # Prix aleatoire entre 10 et 310
    .withColumn("prix", (rand() * 300 + 10).cast("decimal(10,2)"))
    .repartition(200)
)

produits.write.mode("overwrite") \
    .option("header", "true") \
    .csv(f"{BASE_PATH}/produits")

# =========================================================
# ===================== COMMANDES =========================
# =========================================================
# Table de faits commandes
commandes = (
    spark.range(1, NB_COMMANDES + 1)
    .withColumnRenamed("id", "commande_id")
    # Chaque commande est rattachee a un client aleatoire
    .withColumn("client_id", (rand() * NB_CLIENTS + 1).cast("long"))
    .withColumn("date_commande", current_date())
    # 90% des commandes sont validees
    .withColumn(
        "statut",
        expr("CASE WHEN rand() < 0.9 THEN 'VALIDEE' ELSE 'ANNULEE' END")
    )
    .repartition(200)
)

commandes.write.mode("overwrite") \
    .option("header", "true") \
    .csv(f"{BASE_PATH}/commandes")

# =========================================================
# ================= PRODUITS COMMANDES ===================
# =========================================================
# Lignes de commandes (relation N-N commandes / produits)
produits_commandes = (
    spark.range(1, NB_LIGNES_CMD + 1)
    .withColumn("commande_id", (rand() * NB_COMMANDES + 1).cast("long"))
    .withColumn("produit_id", (rand() * NB_PRODUITS + 1).cast("long"))
    .withColumn("quantite", (rand() * 4 + 1).cast("int"))
    .repartition(200)
)

produits_commandes.write.mode("overwrite") \
    .option("header", "true") \
    .csv(f"{BASE_PATH}/produits_commandes")

# =========================================================
# ======================= PANIER ==========================
# =========================================================
# Panier client avant conversion en commande
panier = (
    spark.range(1, NB_PANIERS + 1)
    .withColumnRenamed("id", "panier_id")
    .withColumn("client_id", (rand() * NB_CLIENTS + 1).cast("long"))
    .withColumn("date_creation", current_date())
    .withColumn(
        "statut",
        expr("CASE WHEN rand() < 0.6 THEN 'CONVERTI' ELSE 'ABANDONNE' END")
    )
    .repartition(200)
)

panier.write.mode("overwrite") \
    .option("header", "true") \
    .csv(f"{BASE_PATH}/panier")

# =========================================================
# =============== PRODUITS DANS PANIER ===================
# =========================================================
produits_dans_panier = (
    spark.range(1, NB_LIGNES_CMD + 1)
    .withColumn("panier_id", (rand() * NB_PANIERS + 1).cast("long"))
    .withColumn("produit_id", (rand() * NB_PRODUITS + 1).cast("long"))
    .withColumn("quantite", (rand() * 3 + 1).cast("int"))
    .repartition(200)
)

produits_dans_panier.write.mode("overwrite") \
    .option("header", "true") \
    .csv(f"{BASE_PATH}/produits_dans_panier")

# =========================================================
# ================= NOTATION PRODUIT =====================
# =========================================================
notation_produit = (
    spark.range(1, NB_LIGNES_CMD + 1)
    .withColumn("produit_id", (rand() * NB_PRODUITS + 1).cast("long"))
    .withColumn("client_id", (rand() * NB_CLIENTS + 1).cast("long"))
    .withColumn("note", (rand() * 5 + 1).cast("int"))
    .repartition(200)
)

notation_produit.write.mode("overwrite") \
    .option("header", "true") \
    .csv(f"{BASE_PATH}/notation_produit")

# =========================================================
# ============== HISTORIQUE DES PRIX (SCD) ================
# =========================================================
# Simulation d'une table Slowly Changing Dimension
historique_des_prix = (
    produits
    .select("produit_id", col("prix").alias("prix"))
    .withColumn("date_debut", current_date())
    .withColumn("date_fin", lit(None).cast("date"))
)

historique_des_prix.write.mode("overwrite") \
    .option("header", "true") \
    .csv(f"{BASE_PATH}/historique_des_prix")

# =========================================================
# ================== PRODUITS LIVRES =====================
# =========================================================
# 85% des produits commandes sont livres
produits_livres = (
    produits_commandes
    .withColumn("date_livraison", current_date())
    .filter(rand() < 0.85)
)

produits_livres.write.mode("overwrite") \
    .option("header", "true") \
    .csv(f"{BASE_PATH}/produits_livres")

# =========================================================
# ================= PRODUITS RETOURNES ===================
# =========================================================
# 5% des produits livres sont retournes
produits_retournes = (
    produits_livres
    .filter(rand() < 0.05)
    .withColumn("motif", lit("Defectueux"))
)

produits_retournes.write.mode("overwrite") \
    .option("header", "true") \
    .csv(f"{BASE_PATH}/produits_retournes")

# =====================
# FIN DU SCRIPT
# =====================
spark.stop()
