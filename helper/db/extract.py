from typing import Any, List, Optional

import pandas as pd
import pyodbc


def with_stored_procedure(
    conn_str: str, proc_name: str, params: Optional[List[Any]] = None
) -> pd.DataFrame:
    """
    Executes a stored procedure on Microsoft SQL Server and returns the result as a pandas DataFrame.

    Args:
        conn_str (str): ODBC connection string for SQL Server.
        proc_name (str): Name of the stored procedure to execute.
        params (list or tuple, optional): Parameters to pass to the stored procedure.

    Returns:
        pd.DataFrame: Result set as a DataFrame.
    """
    # Handle None/NULLS in params since we cant do it in JSON config files
    if params is None:
        params = []
    else:
        params = [None if item == "NULL" else item for item in params]
    # Type annotations for connection and cursor
    with pyodbc.connect(conn_str) as conn:  # type: ignore # type: pyodbc.Connection
        cursor = conn.cursor()  # type: pyodbc.Cursor

        placeholders = ",".join(["?"] * len(params)) if params else ""
        sql = (
            f"SET NOCOUNT ON; EXEC {proc_name} {placeholders}"
            if params
            else f"SET NOCOUNT ON; EXEC {proc_name}"
        )

        cursor.execute(
            sql, tuple(params) if params else ()
        )  # Ensures no None is passed directly
        columns = [column[0] for column in cursor.description]  # type: List[str]
        rows = cursor.fetchall()  # type: ignore # type: List[tuple]

        df = pd.DataFrame.from_records(
            rows, columns=columns
        )  # Ensure that from_records is correctly used
    return df


def with_query(
    conn_str: str, sql: str, params: Optional[List[Any]] = None
) -> pd.DataFrame:
    """
    Executes a SQL query on Microsoft SQL Server and returns the result as a pandas DataFrame.

    Args:
        conn_str (str): ODBC connection string for SQL Server.
        query (str): SQL query to execute.
        params (list or tuple, optional): Parameters to pass to the query.

    Returns:
        pd.DataFrame: Result set as a DataFrame.
    """

    with pyodbc.connect(conn_str) as conn:  # type: ignore # type: pyodbc.Connection
        cursor = conn.cursor()  # type: pyodbc.Cursor

        cursor.execute(read_file_content(sql), tuple(params) if params else ())

        columns = [column[0] for column in cursor.description]  # type: List[str]
        rows = cursor.fetchall()  # type: ignore # type: List[tuple]

        df = pd.DataFrame.from_records(
            rows, columns=columns
        )  # Ensure that from_records is correctly used
    return df


def read_file_content(file_path: str) -> str:
    """
    Reads the content of a file and returns it as a string.

    Args:
        file_path: The full path to the file.

    Returns:
        The content of the file as a string, or None if an error occurs.
    """
    with open("./config/queries/" + file_path, "r", encoding="utf-8") as file:
        content = file.read()
        return content
