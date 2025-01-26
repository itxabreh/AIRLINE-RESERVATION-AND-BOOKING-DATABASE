from faker import Faker
import pyodbc
import random

# Replace these variables with your provided SQL Server details
server = 'ADEEL\\SQLEXPRESS'  # Replace with your SQL Server name or IP address
database = 'airline'  # Replace with your database name
username = 'sa'  # Replace with your SQL Server username
password = '12345'  # Replace with your SQL Server password

# Create a connection string
conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Establish the connection
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

fake = Faker()

# Generate fake data and insert into the Passenger table
def insert_fake_passenger_data(num_records):
    for _ in range(num_records):
        full_name = fake.name()
        identification_number = fake.random_int(10000, 99999)  # Generate a random identification number
        # Generate a mobile number within 15 characters limit
        mobile_number = fake.phone_number()[:15]  
        email = fake.email()
        residential_address = fake.address()
        
        # Insert data into the Passenger table
        cursor.execute(
            "INSERT INTO Passenger (full_name, identification_number, mobile_number, email, residential_address) VALUES (?, ?, ?, ?, ?)",
            (full_name, str(identification_number), mobile_number, email, residential_address)
        )
        conn.commit()
        


# Call the function to insert 50 fake records into the Passenger table
insert_fake_passenger_data(50)

# Close the connection
conn.close()
