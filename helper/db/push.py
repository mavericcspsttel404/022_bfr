from typing import Dict, List, Optional, Type

import pandas as pd
import pyodbc

from utils.utils import load_schema


def validate_dataframe_schema(df: pd.DataFrame, schema: Dict[str, Type]) -> None:
    """Validate DataFrame columns and dtypes against expected schema."""
    for col, col_type in schema.items():
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
        # allow NaN values but check non-null values for type
        non_null = df[col].dropna()
        if not non_null.empty and not non_null.map(lambda x: isinstance(x, col_type)).all():
            raise ValueError(f"Column {col} has incorrect type")


def bulk_insert_dataframe(
    conn_str: str,
    table_name: str,
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    expected_schema: Optional[Dict[str, Type]] = None,
    schema_file: Optional[str] = None,
    rename_map: Optional[Dict[str, str]] = None,
) -> None:
    """Insert a pandas DataFrame into a SQL Server table using ``fast_executemany``.

    Args:
        conn_str: ODBC connection string for SQL Server.
        table_name: Name of the destination table.
        df: Data to insert.
        columns: Optional subset of columns from ``df`` to insert.
        expected_schema: Dictionary defining expected column names and Python
            datatypes. Data is validated against this schema before insertion.
        schema_file: Path to a JSON file containing the expected schema. This is
            mutually exclusive with ``expected_schema``.
        rename_map: Mapping of existing column names to the names expected in the
            destination table.
    """
    if rename_map is not None:
        df = df.rename(columns=rename_map)
        if columns is not None:
            columns = [rename_map.get(col, col) for col in columns]

    if columns is None:
        columns = df.columns.tolist()

    if schema_file is not None:
        import os
        import json

        if expected_schema is not None:
            raise ValueError("Provide either expected_schema or schema_file, not both")
        if not os.path.isfile(schema_file):
            raise FileNotFoundError(f"Schema file '{schema_file}' does not exist.")
        try:
            expected_schema = load_schema(schema_file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON from schema file '{schema_file}': {e}")

    if expected_schema is not None:
        validate_dataframe_schema(df, expected_schema)

    placeholders = ",".join(["?"] * len(columns))
    column_names = ",".join(columns)
    insert_sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

    data = [tuple(row) for row in df[columns].itertuples(index=False, name=None)]

    with pyodbc.connect(conn_str) as conn:  # type: ignore # pyodbc.Connection
        cursor = conn.cursor()  # type: ignore # pyodbc.Cursor
        cursor.fast_executemany = True
        cursor.executemany(insert_sql, data)
        conn.commit()
