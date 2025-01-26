from faker import Faker
import random
import pyodbc

fake = Faker()

# Replace these variables with your provided SQL Server details
server = 'ADEEL\\SQLEXPRESS'  # Replace with your SQL Server name or IP address
database = 'airline'  # Replace with your database name
username = 'sa'  # Replace with your SQL Server username
password = '12345'  # Replace with your SQL Server password

# Create a connection string
conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Establish a connection to the SQL Server database
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Simulate and insert data into DenormalizedFlightInfo table
for _ in range(100):  # Simulate data for 100 flights
    flight_number = fake.random_int(1000, 9999)
    airline_name = fake.company()
    departure_location = fake.city()
    departure_date = fake.date_between(start_date='-1y', end_date='+1y')
    departure_time = fake.time_object()
    arrival_location = fake.city()
    arrival_date = fake.date_between(start_date='-1y', end_date='+1y')
    arrival_time = fake.time_object()
    class_type = random.choice(['Business', 'Economy', 'First Class'])
    price = fake.random_int(100, 1000)
    seat_number = fake.random_int(1, 200)
    seat_status = random.choice(['Available', 'Booked'])

    # Insert simulated data into the denormalized table
cursor.execute("""
    INSERT INTO DenormalizedFlightInfo (
        airline_name, departure_location, departure_date, departure_time,
        arrival_location, arrival_date, arrival_time, class_type, price, seat_number, seat_status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    airline_name, departure_location, departure_date, departure_time,
    arrival_location, arrival_date, arrival_time, class_type, price, seat_number, seat_status
))


# Commit the changes and close the connection
conn.commit()
conn.close()
