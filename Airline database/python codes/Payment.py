from faker import Faker
import pyodbc
import random
import decimal
from datetime import datetime

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

# Existing paymentStatusID values from the paymentStatus table
payment_status_ids = [1000, 1001, 1002, ...]  # Replace with actual IDs from paymentStatus table

# Function to insert fake payment data
def insert_fake_payments(num_records):
    for _ in range(num_records):
        amount = decimal.Decimal(random.uniform(50, 5000)).quantize(decimal.Decimal('0.01'))
        payment_date = fake.date_time_between(start_date="-30d", end_date="now")
        payment_status_id = random.choice(payment_status_ids)  # Choose from existing paymentStatusIDs
        payment_method = fake.random_element(['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer'])
        
        # Insert fake data into the Payment table
        cursor.execute(
            "INSERT INTO Payment (amount, payment_date, paymentStatusID, payment_method) VALUES (?, ?, ?, ?)",
            (amount, payment_date, payment_status_id, payment_method)
        )
        conn.commit()

# Call the function to insert fake payment records into the Payment table
insert_fake_payments(50)

# Close the connection
conn.close()
