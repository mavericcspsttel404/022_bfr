import json


def load_config(config_file: str) -> dict:
    """Load the configuration from the JSON file."""
    with open("config/" + config_file, "r") as f:
        return json.load(f)


def read_sql_query(query_file: str) -> str:
    """Reads an SQL query from a .sql file."""
    with open(query_file, "r") as file:
        return file.read()
