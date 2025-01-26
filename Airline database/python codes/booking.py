from faker import Faker
import pyodbc
import random
import string
from datetime import datetime

fake = Faker()

# Replace these variables with your provided SQL Server details
server = 'ADEEL\\SQLEXPRESS'  # Replace with your SQL Server name or IP address
database = 'airline'  # Replace with your database name
username = 'sa'  # Replace with your SQL Server username
password = '12345'  # Replace with your SQL Server password

# Create a connection string
conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
# Establish the connection
try:
    conn = pyodbc.connect(conn_str)
    print("Connection successful!")

    cursor = conn.cursor()

    # Insert data into bookingStatus table
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM bookingStatus)
        BEGIN
            INSERT INTO bookingStatus (statusName)
            VALUES ('Booked'), ('Canceled')
        END
    """)
    conn.commit()
    print("Data inserted into bookingStatus table successfully!")

    # Fetching necessary IDs for Booking insertion
    cursor.execute("SELECT payment_id, paymentStatusID FROM Payment")
    payment_data = cursor.fetchall()

    # Insert data into Booking table
    for payment_id, payment_status_id in payment_data:
        booking_status_id = 1 if payment_status_id != 3 else 2  # 3 is the paymentStatusID for 'Failed'

        cursor.execute("""
            INSERT INTO Booking (payment_id, booking_date, bookingStatusID)
            VALUES (?, ?, ?)
        """, (payment_id, datetime.now(), booking_status_id))

    conn.commit()
    print("Data inserted into Booking table successfully!")

    conn.close()

except pyodbc.Error as ex:
    print("Error connecting to the database:", ex)