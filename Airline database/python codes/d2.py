from faker import Faker
import pyodbc
from datetime import datetime, timedelta
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

# Custom lists for airline names, departure, and arrival locations
airline_names = ["Qatar Airways", "Singapore Airlines", "PIA", "Emirates", "AirAsia", "Japan Airlines",
                 "Turkish airlines", "AirBlue", "Fly Jinnah", "Royal Airlines"]  # Add more airline names as needed
departure_locations = ["Japan", "China", "India", "United Arab Emirates", "Saudi Arabia", "South Korea",
                       "Turkiye", "Thailand", "Thailand", "Pakistan", "Malaysia"]  # Add more departure locations as needed
arrival_locations = ["Germany", "Italy", "Spain", "Egypt", "America", "Dubai", "Qatar", "Iran", "Iraq",
                     "Oman"]  # Add more arrival locations as needed

# Establish the connection
try:
    conn = pyodbc.connect(conn_str)
    print("Connection successful!")

    cursor = conn.cursor()

    # Generate flight data for a year
    current_date = datetime.now().date()
    end_date = current_date + timedelta(days=2000)

    while current_date < end_date:
        airline_name = random.choice(airline_names)
        departure_location = random.choice(departure_locations)
        arrival_location = random.choice(arrival_locations)

        random_letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        random_digits = ''.join(random.choices(string.digits, k=3))
        flight_number = random_letters + random_digits

        departure_date = current_date
        departure_time = fake.time_object(end_datetime=datetime.combine(current_date, datetime.min.time()))
        departure_time_str = departure_time.strftime("%H:%M:%S")

        arrival_date = current_date + timedelta(days=random.randint(1, 5))
        arrival_time = fake.time_object(end_datetime=datetime.combine(arrival_date, datetime.min.time()))
        arrival_time_str = arrival_time.strftime("%H:%M:%S")

        cursor.execute("""
        INSERT INTO FlightInformation 
        (airline_name, flight_number, departure_location, departure_date, departure_time, arrival_location, arrival_date, arrival_time) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (airline_name, flight_number, departure_location, departure_date, departure_time_str,
              arrival_location, arrival_date, arrival_time_str))

        cursor.execute("SELECT @@IDENTITY AS ID")
        flight_id = cursor.fetchone()[0]

        class_types = ['Business', 'Economy', 'First Class']
        existing_classes = set()
        for class_type in class_types:
            if class_type not in existing_classes:
                cursor.execute("""
                    INSERT INTO FlightClass (flight_id, class_type)
                    VALUES (?, ?)
                """, (flight_id, class_type))

                cursor.execute("SELECT @@IDENTITY AS ID")
                flight_class_id = cursor.fetchone()[0]

                existing_classes.add(class_type)

            prices = {
                'Business': round(random.uniform(2000, 2500)),  # Business Class price range
                'Economy': round(random.uniform(800, 1000)),  # Economy Class price range
                'First Class': round(random.uniform(400, 600))  # First Class price range
            }

            effective_date = current_date

            for class_type, price in prices.items():
                # Inserting price with $ sign
                cursor.execute("""
                    INSERT INTO Price (flight_class_id, price, effective_date)
                    VALUES (?, ?, ?)
                """, (flight_class_id, f'${price}', effective_date))

        current_date += timedelta(days=random.randint(1, 14))  # Varying days between flights

    conn.commit()
    print("Data inserted successfully!")

    conn.close()

except pyodbc.Error as ex:
    print("Error connecting to the database:", ex)
