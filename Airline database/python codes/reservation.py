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

    # Insert data into reservationStatus table
    cursor.execute("""
        INSERT INTO reservationStatus (statusName)
        VALUES ('Confirmed'), ('Cancelled'), ('Pending')
    """)
    conn.commit()
    print("Data inserted into reservationStatus table successfully!")

    # Fetching necessary IDs for reservation insertion
    cursor.execute("SELECT passenger_id FROM Passenger")  # Fetching existing passenger IDs
    passenger_ids = [id[0] for id in cursor.fetchall()]

    cursor.execute("SELECT seat_id FROM flightSeats")  # Fetching existing seat IDs
    seat_ids = [id[0] for id in cursor.fetchall()]

    cursor.execute("SELECT payment_id FROM payment")  # Fetching existing payment IDs
    payment_ids = [id[0] for id in cursor.fetchall()]

    cursor.execute("SELECT reservationStatusID FROM reservationStatus")  # Fetching existing reservationStatus IDs
    status_ids = [id[0] for id in cursor.fetchall()]

    # Insert data into Reservation table
    for _ in range(50):  # Inserting 50 reservation records as an example
        passenger_id = random.choice(passenger_ids)
        seat_id = random.choice(seat_ids)
        payment_id = random.choice(payment_ids)
        status_id = random.choice(status_ids)

        cursor.execute("""
            INSERT INTO Reservation (passenger_id, seat_id, payment_id, reservationStatusID)
            VALUES (?, ?, ?, ?)
        """, (passenger_id, seat_id, payment_id, status_id))

    conn.commit()
    print("Data inserted into Reservation table successfully!")

    conn.close()

except pyodbc.Error as ex:
    print("Error connecting to the database:", ex)