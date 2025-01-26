import pyodbc
from faker import Faker
import random
from datetime import datetime, timedelta

# Connect to your SQL Server database
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=ADEEL\\SQLEXPRESS;'
                      'DATABASE=airline;'
                      'UID=sa;'
                      'PWD=12345')

cursor = conn.cursor()

# Use Faker to generate fake data
fake = Faker()

# Generate and insert fake notification data for confirmed bookings (payment confirmed)
for _ in range(10):  # Inserting 10 fake notifications for demonstration
    booking_id = random.randint(1, 10)  # Replace with your actual booking IDs range

    # Query the database to check if payment for the booking is confirmed
    payment_query = f"SELECT payment_status FROM Payment WHERE booking_id = {booking_id}"
    cursor.execute(payment_query)
    payment_status = cursor.fetchone()

    if payment_status and payment_status.payment_status == 'Confirmed':
        passenger_id = random.randint(1, 10)  # Replace with your actual passenger IDs range
        notification_date = fake.date_time_between(start_date='-30d', end_date='now')

        # Construct SQL query to insert fake notification data
        query = f"INSERT INTO Notifications (booking_id, passenger_id, notification_date, notification_status_confirmed) VALUES ({booking_id}, {passenger_id}, '{notification_date}', 'Booking Confirmed')"
        
        # Execute the SQL query
        cursor.execute(query)

# Commit the changes and close the connection
conn.commit()
conn.close()