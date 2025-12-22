"""
=========================================================
SCRIPT : generate_raw_data.py
OBJECTIF :
- Générer toutes les données brutes (RAW) en CSV
- Simuler une plateforme e-commerce à grande échelle
- Compatible Spark / Docker / Airflow
AUTEUR : Rooldy
=========================================================
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, rand, concat, current_date, expr
from pyspark.sql.types import StringType, IntegerType, DecimalType, DateType

# =====================
# INITIALISATION SPARK
# =====================
spark = (
    SparkSession.builder
    .appName("GenerateRawCSV")
    .config("spark.sql.shuffle.partitions", "200")
    .config("spark.sql.session.timeZone", "UTC")
    .getOrCreate()
)

BASE_PATH = "/app/data/raw"

# =====================
# PARAMETRES DE VOLUMETRIE
# =====================
NB_CLIENTS = 1_000_000
NB_PRODUITS = 200_000
NB_COMMANDES = 3_000_000
NB_LIGNES_CMD = 8_000_000
NB_PANIERS = 1_500_000
NB_PAIEMENTS = int(NB_COMMANDES * 0.95)
NB_LIVRAISONS = int(NB_COMMANDES * 0.85)
NB_PROMOTIONS = 5_000
NB_EVENTS = 20_000_000
NB_FOURNISSEURS = 5_000
NB_ENTREPOTS = 200

# =====================
# DIMENSIONS
# =====================

# Clients
dim_clients = (
    spark.range(1, NB_CLIENTS + 1)
    .withColumnRenamed("id", "client_id")
    .withColumn("nom", concat(lit("Client_"), col("client_id")))
    .withColumn("email", concat(lit("client"), col("client_id"), lit("@mail.com")))
    .withColumn("pays", lit("FR"))
    .withColumn("date_creation", current_date())
    .withColumn("statut_client", expr("CASE WHEN rand() < 0.95 THEN 'ACTIF' ELSE 'INACTIF' END"))
    .withColumn("segment_client", expr("CASE WHEN rand() < 0.7 THEN 'STANDARD' ELSE 'PREMIUM' END"))
)
dim_clients.write.mode("overwrite").option("header", "true").csv(f"{BASE_PATH}/dim_clients")

# Produits
dim_produits = (
    spark.range(1, NB_PRODUITS + 1)
    .withColumnRenamed("id", "produit_id")
    .withColumn("nom_produit", concat(lit("Produit_"), col("produit_id")))
    .withColumn("categorie", expr("""
        CASE
            WHEN produit_id % 3 = 0 THEN 'Tech'
            WHEN produit_id % 3 = 1 THEN 'Maison'
            ELSE 'Mode'
        END
    """))
    .withColumn("sous_categorie", expr("CASE WHEN produit_id % 2 = 0 THEN 'Premium' ELSE 'Standard' END"))
    .withColumn("marque", concat(lit("Marque_"), (col("produit_id") % 50)))
    .withColumn("prix_actuel", (rand() * 300 + 10).cast(DecimalType(10,2)))
    .withColumn("date_creation", current_date())
    .withColumn("actif", lit(True))
)
dim_produits.write.mode("overwrite").option("header", "true").csv(f"{BASE_PATH}/dim_produits")

# Fournisseurs
dim_fournisseurs = (
    spark.range(1, NB_FOURNISSEURS + 1)
    .withColumnRenamed("id", "fournisseur_id")
    .withColumn("nom_fournisseur", concat(lit("Fournisseur_"), col("fournisseur_id")))
    .withColumn("pays", lit("FR"))
    .withColumn("contact_email", concat(lit("contact"), col("fournisseur_id"), lit("@mail.com")))
    .withColumn("date_creation", current_date())
    .withColumn("actif", lit(True))
)
dim_fournisseurs.write.mode("overwrite").option("header", "true").csv(f"{BASE_PATH}/dim_fournisseurs")

# Entrepôts
dim_entrepots = (
    spark.range(1, NB_ENTREPOTS + 1)
    .withColumnRenamed("id", "entrepot_id")
    .withColumn("nom_entrepot", concat(lit("Entrepot_"), col("entrepot_id")))
    .withColumn("ville", lit("Paris"))
    .withColumn("pays", lit("FR"))
    .withColumn("capacite_stock", (rand() * 500_000 + 50_000).cast(IntegerType()))
    .withColumn("date_creation", current_date())
    .withColumn("actif", lit(True))
)
dim_entrepots.write.mode("overwrite").option("header", "true").csv(f"{BASE_PATH}/dim_entrepots")

# Promotions
dim_promotions = (
    spark.range(1, NB_PROMOTIONS + 1)
    .withColumnRenamed("id", "promotion_id")
    .withColumn("type_promotion", expr("CASE WHEN promotion_id % 3 = 0 THEN 'FLASH' WHEN promotion_id % 3 = 1 THEN 'COUPON' ELSE 'SOLDES' END"))
    .withColumn("taux_reduction", (rand() * 30 + 5).cast(DecimalType(5,2)))
    .withColumn("date_debut", current_date())
    .withColumn("date_fin", current_date())
    .withColumn("actif", lit(True))
)
dim_promotions.write.mode("overwrite").option("header", "true").csv(f"{BASE_PATH}/dim_promotions")

# Moyens de paiement
dim_moyens_paiement = (
    spark.range(1, 6)
    .withColumnRenamed("id", "paiement_id")
    .withColumn("type_paiement", expr("CASE WHEN paiement_id % 2 = 0 THEN 'CB' ELSE 'PAYPAL' END"))
    .withColumn("fournisseur_paiement", lit("Banque_X"))
    .withColumn("devise", lit("EUR"))
    .withColumn("actif", lit(True))
)
dim_moyens_paiement.write.mode("overwrite").option("header", "true").csv(f"{BASE_PATH}/dim_moyens_paiement")

# =====================
# FAITS
# =====================

# Commandes
fact_commandes = (
    spark.range(1, NB_COMMANDES + 1)
    .withColumnRenamed("id", "commande_id")
    .withColumn("client_id", (rand() * NB_CLIENTS + 1).cast("long"))
    .withColumn("date_commande", current_date())
    .withColumn("statut_commande", expr("CASE WHEN rand() < 0.9 THEN 'VALIDEE' ELSE 'ANNULEE' END"))
    .withColumn("montant_total", (rand() * 1000 + 50).cast(DecimalType(10,2)))
    .withColumn("nb_produits", (rand() * 5 + 1).cast(IntegerType()))
    .withColumn("source_commande", expr("CASE WHEN rand() < 0.5 THEN 'WEB' ELSE 'APP' END"))
)
fact_commandes.write.mode("overwrite").option("header", "true").csv(f"{BASE_PATH}/fact_commandes")

# Produits commandes
fact_produits_commandes = (
    spark.range(1, NB_LIGNES_CMD + 1)
    .withColumnRenamed("id", "ligne_commande_id")
    .withColumn("commande_id", (rand() * NB_COMMANDES + 1).cast("long"))
    .withColumn("produit_id", (rand() * NB_PRODUITS + 1).cast("long"))
    .withColumn("quantite", (rand() * 4 + 1).cast(IntegerType()))
    .withColumn("prix_unitaire", (rand() * 300 + 10).cast(DecimalType(10,2)))
    .withColumn("montant_ligne", (col("quantite") * col("prix_unitaire")).cast(DecimalType(10,2)))
)
fact_produits_commandes.write.mode("overwrite").option("header", "true").csv(f"{BASE_PATH}/fact_produits_commandes")

# Panier
fact_panier = (
    spark.range(1, NB_PANIERS + 1)
    .withColumnRenamed("id", "panier_id")
    .withColumn("client_id", (rand() * NB_CLIENTS + 1).cast("long"))
    .withColumn("date_creation", current_date())
    .withColumn("statut_panier", expr("CASE WHEN rand() < 0.6 THEN 'CONVERTI' ELSE 'ABANDONNE' END"))
    .withColumn("montant_panier", (rand() * 500 + 20).cast(DecimalType(10,2)))
)
fact_panier.write.mode("overwrite").option("header", "true").csv(f"{BASE_PATH}/fact_panier")

# Produits dans panier
fact_produits_dans_panier = (
    spark.range(1, NB_LIGNES_CMD + 1)
    .withColumn("panier_id", (rand() * NB_PANIERS + 1).cast("long"))
    .withColumn("produit_id", (rand() * NB_PRODUITS + 1).cast("long"))
    .withColumn("quantite", (rand() * 3 + 1).cast(IntegerType()))
    .withColumn("prix_estime", (rand() * 300 + 10).cast(DecimalType(10,2)))
)
fact_produits_dans_panier.write.mode("overwrite").option("header", "true").csv(f"{BASE_PATH}/fact_produits_dans_panier")

# Produits livrés
fact_produits_livres = (
    spark.range(1, NB_LIVRAISONS + 1)
    .withColumnRenamed("id", "livraison_id")
    .withColumn("commande_id", (rand() * NB_COMMANDES + 1).cast("long"))
    .withColumn("produit_id", (rand() * NB_PRODUITS + 1).cast("long"))
    .withColumn("date_livraison", current_date())
    .withColumn("delai_livraison", (rand() * 5 + 1).cast(IntegerType()))
    .withColumn("statut_livraison", expr("CASE WHEN rand() < 0.9 THEN 'LIVREE' ELSE 'RETARDEE' END"))
)
fact_produits_livres.write.mode("overwrite").option("header", "true").csv(f"{BASE_PATH}/fact_produits_livres")

# Produits retournés
fact_produits_retournes = (
    spark.range(1, NB_LIVRAISONS // 5 + 1)
    .withColumnRenamed("id", "retour_id")
    .withColumn("commande_id", (rand() * NB_COMMANDES + 1).cast("long"))
    .withColumn("produit_id", (rand() * NB_PRODUITS + 1).cast("long"))
    .withColumn("date_retour", current_date())
    .withColumn("motif_retour", expr("CASE WHEN rand() < 0.5 THEN 'DEFAUT' ELSE 'INSATISFACTION' END"))
    .withColumn("montant_rembourse", (rand() * 300 + 10).cast(DecimalType(10,2)))
)
fact_produits_retournes.write.mode("overwrite").option("header", "true").csv(f"{BASE_PATH}/fact_produits_retournes")

# Notation produit
fact_notation_produit = (
    spark.range(1, NB_LIGNES_CMD + 1)
    .withColumnRenamed("id", "notation_id")
    .withColumn("produit_id", (rand() * NB_PRODUITS + 1).cast("long"))
    .withColumn("client_id", (rand() * NB_CLIENTS + 1).cast("long"))
    .withColumn("note", (rand() * 5 + 1).cast(IntegerType()))
    .withColumn("commentaire", concat(lit("Avis_"), col("notation_id")))
    .withColumn("date_notation", current_date())
)
fact_notation_produit.write.mode("overwrite").option("header", "true").csv(f"{BASE_PATH}/fact_notation_produit")

# Paiements
fact_paiements = (
    spark.range(1, NB_PAIEMENTS + 1)
    .withColumnRenamed("id", "transaction_id")
    .withColumn("commande_id", (rand() * NB_COMMANDES + 1).cast("long"))
    .withColumn("paiement_id", (rand() * 5 + 1).cast("long"))
    .withColumn("montant", (rand() * 1000 + 20).cast(DecimalType(10,2)))
    .withColumn("statut_paiement", expr("CASE WHEN rand() < 0.9 THEN 'OK' ELSE 'KO' END"))
    .withColumn("date_paiement", current_date())
)
fact_paiements.write.mode("overwrite").option("header", "true").csv(f"{BASE_PATH}/fact_paiements")

# Livraisons détaillées
fact_livraisons_detaillees = (
    spark.range(1, NB_LIVRAISONS + 1)
    .withColumnRenamed("id", "livraison_id")
    .withColumn("commande_id", (rand() * NB_COMMANDES + 1).cast("long"))
    .withColumn("entrepot_id", (rand() * NB_ENTREPOTS + 1).cast("long"))
    .withColumn("transporteur", concat(lit("Transporteur_"), (rand() * 10 + 1).cast("int")))
    .withColumn("date_expedition", current_date())
    .withColumn("date_livraison", current_date())
    .withColumn("cout_livraison", (rand() * 50 + 5).cast(DecimalType(10,2)))
)
fact_livraisons_detaillees.write.mode("overwrite").option("header", "true").csv(f"{BASE_PATH}/fact_livraisons_detaillees")

# Evenements logs (streaming simulé)
fact_evenements_logs = (
    spark.range(1, NB_EVENTS + 1)
    .withColumnRenamed("id", "event_id")
    .withColumn("type_evenement", expr("CASE WHEN rand() < 0.5 THEN 'CLICK' ELSE 'ACHAT' END"))
    .withColumn("entite", expr("CASE WHEN rand() < 0.5 THEN 'PRODUIT' ELSE 'CLIENT' END"))
    .withColumn("entite_id", (rand() * NB_CLIENTS + 1).cast("long"))
    .withColumn("timestamp_event", current_date())
    .withColumn("source_event", expr("CASE WHEN rand() < 0.5 THEN 'WEB' ELSE 'APP' END"))
    .withColumn("payload_json", concat(lit("{\"value\":"), col("event_id"), lit("}")))
)
fact_evenements_logs.write.mode("overwrite").option("header", "true").csv(f"{BASE_PATH}/fact_evenements_logs")

# Historique prix produits (SCD)
dim_scd_historique_prix_produits = (
    dim_produits.select("produit_id", col("prix_actuel").alias("prix"))
    .withColumn("date_debut", current_date())
    .withColumn("date_fin", lit(None).cast(DateType()))
    .withColumn("is_current", lit(True))
)
dim_scd_historique_prix_produits.write.mode("overwrite").option("header", "true").csv(f"{BASE_PATH}/scd_historique_prix_produits")

# =====================
# FIN DU SCRIPT
# =====================
spark.stop()
print("Génération CSV RAW terminée avec succès pour toutes les tables !")
