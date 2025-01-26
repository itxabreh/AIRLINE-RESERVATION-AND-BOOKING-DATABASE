from faker import Faker
import random
import decimal
import pyodbc

# Establish a connection to your SQL Server database
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=ADEEL\\SQLEXPRESS;'
                      'DATABASE=airline;'
                      'UID=sa;'
                      'PWD=12345;')


cursor = conn.cursor()

# Create a Faker instance
fake = Faker()

# Insert data into paymentStatus table
statuses = ['Paid', 'Pending', 'Failed']
for status in statuses:
    cursor.execute("INSERT INTO paymentStatus (statusName) VALUES (?)", status)

# Commit the changes for paymentStatus table
conn.commit()

# Insert data into Payment table
number_of_payments = 10000  # Total number of payments
failed_payments = int(number_of_payments * 0.1)  # 10% of payments are failed

for _ in range(number_of_payments):
    amount = round(random.uniform(10, 1000), 2)
    payment_date = fake.date_time_between(start_date='-1y', end_date='now')
    payment_status = random.choice(statuses)
    payment_method = fake.random_element(elements=('Credit Card', 'Debit Card', 'PayPal'))

    # For 10% of payments, set the status as 'Failed'
    if failed_payments > 0:
        payment_status = 'Failed'
        failed_payments -= 1

    cursor.execute("INSERT INTO Payment (amount, payment_date, paymentStatusID, payment_method) VALUES (?, ?, (SELECT paymentStatusID FROM paymentStatus WHERE statusName = ?), ?)",
                   amount, payment_date, payment_status, payment_method)

# Commit the changes for Payment table
conn.commit()

# Close the connection
conn.close()

print("Data insertion completed.")

