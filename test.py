from utils.db.exec_storedproc import exec_stored_procedure_to_df

# Example connection string (update with your server, database, user, and password)
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=your_server;"
    "DATABASE=your_database;"
    "UID=your_username;"
    "PWD=your_password"
)

# Example stored procedure and parameters
proc_name = "YourStoredProcedureName"
params = ["param1", "param2"]  # Replace with actual parameters or leave empty if none

df = exec_stored_procedure_to_df(conn_str, proc_name, params)
print(df)
