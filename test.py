import logging

import pyodbc

logging.basicConfig(level=logging.DEBUG)
# Define the connection details
server = "127.0.0.1"
# server = "10.89.4.2"
port = "1433"
database = "master"
username = "sa"
password = "YourStrong!Passw0rd"

connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server},{port};DATABASE={database};UID={username};PWD={password}"  # ;TrustServerCertificate=yes"

# Try to establish the connection
try:
    conn = pyodbc.connect(connection_string)
    print("Connected to SQL Server")
except Exception as e:
    print(f"Error: {e}")
else:
    # Only attempt to close connection if it was successful
    conn.close()
    print("Connection closed")
