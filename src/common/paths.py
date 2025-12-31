from pathlib import Path
import os

# =========================
# BASE PATH (configurable)
# =========================
BASE_DATA_PATH = Path(
    os.getenv("DATA_BASE_PATH", "/app/data")
)

# =========================
# ZONES DATA LAKE
# =========================
RAW_PATH = BASE_DATA_PATH / "raw"
BRONZE_PATH = BASE_DATA_PATH / "bronze"
SILVER_PATH = BASE_DATA_PATH / "silver"
GOLD_PATH = BASE_DATA_PATH / "gold"

# =========================
# HELPERS
# =========================
def raw_table_path(table_name: str) -> str:
    return str(RAW_PATH / table_name)


def bronze_table_path(table_name: str) -> str:
    return str(BRONZE_PATH / table_name)


def silver_table_path(table_name: str) -> str:
    return str(SILVER_PATH / table_name)


def gold_table_path(table_name: str) -> str:
    return str(GOLD_PATH / table_name)
