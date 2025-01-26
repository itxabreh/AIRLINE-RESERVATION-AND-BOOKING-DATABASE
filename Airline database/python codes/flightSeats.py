from faker import Faker
import pyodbc
import random
import string

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

    # Generate flight seats data
    cursor.execute("SELECT flight_class_id, flight_id FROM FlightClass")  # Fetching existing flight class and flight IDs
    flight_classes = cursor.fetchall()

    for flight_class in flight_classes:
        flight_class_id, flight_id = flight_class
        seat_status = random.choice(['Available', 'Booked'])
        seat_number = fake.random_element(["A", "B", "C", "D", "E"]) + str(fake.random_int(1, 200))  # Generating random seat numbers
        
        cursor.execute("""
            INSERT INTO flightSeats (flight_class_id, seat_number, flight_id, seat_status)
            VALUES (?, ?, ?, ?)
        """, (flight_class_id, seat_number, flight_id, seat_status))

    conn.commit()
    print("Flight seats data inserted successfully!")

    conn.close()

except pyodbc.Error as ex:
    print("Error connecting to the database:", ex)