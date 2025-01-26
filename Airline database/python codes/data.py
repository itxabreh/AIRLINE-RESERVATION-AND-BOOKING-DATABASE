import pyodbc

# Connection parameters
server = 'ADEEL\\SQLEXPRESS'
database = 'airline'
username = 'sa'
password = '12345'

# Create a connection string
conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Establish the connection
try:
    conn = pyodbc.connect(conn_str)
    print("Connection successful! Congratulations!")
    cursor = conn.cursor()

    # Example query
    cursor.execute("SELECT @@version;")
    row = cursor.fetchone()
    while row:
        print(row[0])
        row = cursor.fetchone()

except pyodbc.Error as ex:
    print("Error connecting to the database:", ex)

finally:
    # Close the connection in the 'finally' block to ensure it happens
    if 'conn' in locals():
        conn.close()
        print("Connection closed.")
