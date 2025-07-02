import json
from typing import Dict, Type

PYTHON_TYPE_MAP: dict[str, Type] = {
    "int": int,
    "float": float,
    "str": str,
    "bool": bool,
}


def load_config(config_file: str) -> dict:
    """Load the configuration from the JSON file."""
    with open(config_file, "r") as f:
        return json.load(f)


def read_sql_query(query_file: str) -> str:
    """Reads an SQL query from a .sql file."""
    with open(query_file, "r") as file:
        return file.read()


def load_schema(schema_file: str) -> Dict[str, Type]:
    """Load a JSON schema file and convert type strings to Python types."""
    raw_schema = load_config(schema_file)
    return {col: PYTHON_TYPE_MAP[type_str] for col, type_str in raw_schema.items()}
