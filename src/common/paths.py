from pathlib import Path

BASE_DATA_PATH = Path("/app/data")

RAW_PATH = BASE_DATA_PATH / "raw"
BRONZE_PATH = BASE_DATA_PATH / "bronze"
SILVER_PATH = BASE_DATA_PATH / "silver"
GOLD_PATH = BASE_DATA_PATH / "gold"


def raw_table_path(table_name: str) -> str:
    return str(RAW_PATH / table_name)


def bronze_table_path(table_name: str) -> str:
    return str(BRONZE_PATH / table_name)


def silver_table_path(table_name: str) -> str:
    return str(SILVER_PATH / table_name)


def gold_table_path(table_name: str) -> str:
    return str(GOLD_PATH / table_name)
