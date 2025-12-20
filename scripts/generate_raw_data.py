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
# VOLUMÉTRIE EXTENSION
# =====================
NB_PAIEMENTS = int(NB_COMMANDES * 0.95)
NB_LIVRAISONS = int(NB_COMMANDES * 0.85)
NB_PROMOTIONS = 5_000
NB_EVENTS = 20_000_000
NB_FOURNISSEURS = 5_000
NB_ENTREPOTS = 200

# =====================
# FOURNISSEURS
# =====================
fournisseurs = spark.range(1, NB_FOURNISSEURS + 1) \
    .withColumnRenamed("id", "fournisseur_id") \
    .withColumn("nom_fournisseur", concat(lit("Fournisseur_"), col("fournisseur_id"))) \
    .withColumn("pays", lit("FR")) \
    .withColumn("type_fournisseur", expr("CASE WHEN fournisseur_id % 2 = 0 THEN 'Local' ELSE 'International' END"))

fournisseurs.write.mode("overwrite").option("header", "true") \
    .csv(f"{BASE_PATH}/fournisseurs")

# =====================
# ENTREPOTS
# =====================
entrepots = spark.range(1, NB_ENTREPOTS + 1) \
    .withColumnRenamed("id", "entrepot_id") \
    .withColumn("nom_entrepot", concat(lit("Entrepot_"), col("entrepot_id"))) \
    .withColumn("ville", lit("Paris")) \
    .withColumn("pays", lit("FR")) \
    .withColumn("capacite_stock", (rand() * 500_000 + 50_000).cast("int"))

entrepots.write.mode("overwrite").option("header", "true") \
    .csv(f"{BASE_PATH}/entrepots")

# =====================
# PAIEMENTS
# =====================
paiements = spark.range(1, NB_PAIEMENTS + 1) \
    .withColumnRenamed("id", "paiement_id") \
    .withColumn("commande_id", (rand() * NB_COMMANDES + 1).cast("long")) \
    .withColumn("client_id", (rand() * NB_CLIENTS + 1).cast("long")) \
    .withColumn("montant", (rand() * 300 + 20).cast("decimal(10,2)")) \
    .withColumn("devise", lit("EUR")) \
    .withColumn("mode_paiement", expr("CASE WHEN rand() < 0.6 THEN 'CB' WHEN rand() < 0.85 THEN 'PAYPAL' ELSE 'VIREMENT' END")) \
    .withColumn("statut_paiement", expr("CASE WHEN rand() < 0.95 THEN 'ACCEPTE' ELSE 'REFUSE' END")) \
    .withColumn("date_paiement", current_date())

paiements.write.mode("overwrite").option("header", "true") \
    .csv(f"{BASE_PATH}/paiements")

# =====================
# LIVRAISONS DETAILLEES
# =====================
livraisons = spark.range(1, NB_LIVRAISONS + 1) \
    .withColumnRenamed("id", "livraison_id") \
    .withColumn("commande_id", (rand() * NB_COMMANDES + 1).cast("long")) \
    .withColumn("entrepot_id", (rand() * NB_ENTREPOTS + 1).cast("long")) \
    .withColumn("date_expedition", current_date()) \
    .withColumn("date_livraison_prevue", current_date()) \
    .withColumn("date_livraison_reelle", current_date()) \
    .withColumn("statut_livraison", expr("CASE WHEN rand() < 0.9 THEN 'LIVREE' ELSE 'EN_RETARD' END")) \
    .withColumn("delai_livraison", (rand() * 5 + 1).cast("int"))

livraisons.write.mode("overwrite").option("header", "true") \
    .csv(f"{BASE_PATH}/livraisons_detaillees")

# =====================
# PROMOTIONS
# =====================
promotions = spark.range(1, NB_PROMOTIONS + 1) \
    .withColumnRenamed("id", "promotion_id") \
    .withColumn("type_promotion", expr("CASE WHEN promotion_id % 3 = 0 THEN 'FLASH' WHEN promotion_id % 3 = 1 THEN 'COUPON' ELSE 'SOLDES' END")) \
    .withColumn("canal", expr("CASE WHEN promotion_id % 2 = 0 THEN 'EMAIL' ELSE 'APP' END")) \
    .withColumn("date_debut", current_date()) \
    .withColumn("date_fin", current_date())

promotions.write.mode("overwrite").option("header", "true") \
    .csv(f"{BASE_PATH}/promotions")

# =====================
# PROMOTIONS APPLIQUEES
# =====================
promos_appliquees = spark.range(1, NB_LIGNES_CMD + 1) \
    .withColumn("commande_id", (rand() * NB_COMMANDES + 1).cast("long")) \
    .withColumn("produit_id", (rand() * NB_PRODUITS + 1).cast("long")) \
    .withColumn("promotion_id", (rand() * NB_PROMOTIONS + 1).cast("long")) \
    .withColumn("taux_remise", (rand() * 30 + 5).cast("decimal(5,2)")) \
    .withColumn("montant_remise", (rand() * 50 + 5).cast("decimal(10,2)"))

promos_appliquees.write.mode("overwrite").option("header", "true") \
    .csv(f"{BASE_PATH}/promotions_appliquees")

# =====================
# EVENTS LOGS
# =====================
events = spark.range(1, NB_EVENTS + 1) \
    .withColumnRenamed("id", "event_id") \
    .withColumn("client_id", (rand() * NB_CLIENTS + 1).cast("long")) \
    .withColumn("produit_id", (rand() * NB_PRODUITS + 1).cast("long")) \
    .withColumn("commande_id", (rand() * NB_COMMANDES + 1).cast("long")) \
    .withColumn("event_type", expr("CASE WHEN rand() < 0.4 THEN 'VIEW' WHEN rand() < 0.6 THEN 'ADD_TO_CART' WHEN rand() < 0.8 THEN 'PURCHASE' ELSE 'CLICK' END")) \
    .withColumn("event_timestamp", expr("current_timestamp()")) \
    .withColumn("device", expr("CASE WHEN rand() < 0.5 THEN 'MOBILE' ELSE 'DESKTOP' END")) \
    .withColumn("source", expr("CASE WHEN rand() < 0.5 THEN 'WEB' ELSE 'APP' END"))

events.write.mode("overwrite").option("header", "true") \
    .csv(f"{BASE_PATH}/events_logs")

# =====================
# FIN DU SCRIPT
# =====================
spark.stop()
