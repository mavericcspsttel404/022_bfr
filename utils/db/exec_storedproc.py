
import pyodbc
import pandas as pd

def exec_stored_procedure_to_df(conn_str, proc_name, params=None):
    """
    Executes a stored procedure on Microsoft SQL Server and returns the result as a pandas DataFrame.
    
    Args:
        conn_str (str): ODBC connection string for SQL Server.
        proc_name (str): Name of the stored procedure to execute.
        params (list or tuple, optional): Parameters to pass to the stored procedure.
    
    Returns:
        pd.DataFrame: Result set as a DataFrame.
    """
    if params is None:
        params = []
    with pyodbc.connect(conn_str) as conn:
        cursor = conn.cursor()
        placeholders = ','.join(['?'] * len(params))
        sql = f"EXEC {proc_name} {placeholders}" if params else f"EXEC {proc_name}"
        cursor.execute(sql, params)
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        df = pd.DataFrame.from_records(rows, columns=columns)
    return df
