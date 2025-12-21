import os

# Chemin de base du projet (où se trouve le dossier data)
BASE_DIR = "/app/data"

# Structure des dossiers par couche
BRONZE_DIR = os.path.join(BASE_DIR, "bronze")
SILVER_DIR = os.path.join(BASE_DIR, "silver")
GOLD_DIR = os.path.join(BASE_DIR, "gold")

# Listes de tables par type
TABLES_DIMENSIONS = [
    "dim_clients",
    "dim_produits",
    "dim_fournisseurs",
    "dim_entrepots",
    "dim_promotions",
    "dim_moyens_paiement"
]

TABLES_FACTS = [
    "fact_commandes",
    "fact_produits_commandes",
    "fact_panier",
    "fact_produits_dans_panier",
    "fact_produits_livres",
    "fact_produits_retournes",
    "fact_notation_produit",
    "fact_paiements",
    "fact_livraisons_detaillees",
    "fact_evenements_logs"
]

TABLES_HISTORIQUE = [
    "scd_historique_prix_produits"
]

# Fonction utilitaire pour générer les chemins complets
def get_paths(table_name: str):
    """
    Retourne un dictionnaire avec les chemins bronze, silver et gold pour une table donnée.
    """
    return {
        "bronze": os.path.join(BRONZE_DIR, table_name),
        "silver": os.path.join(SILVER_DIR, table_name),
        "gold": os.path.join(GOLD_DIR, table_name),
    }

# Exemple d'utilisation
if __name__ == "__main__":
    print("Exemple chemins pour dim_clients :")
    print(get_paths("dim_clients"))
