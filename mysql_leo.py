import requests
import mysql.connector
import json
from datetime import datetime, timedelta

# Step 1: Make the API request and get the data
api_url = "http://new2.leopardscod.com/webservice/trackBookedPacketGulAhmed"
from_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
to_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')

api_params = {
    #"from_date": "2023-01-10",
    #"to_date": "2023-01-10",
    'from_date': from_date,
    'to_date': to_date,
    "api_key": "0E33E3FB5F99FC57D18134F753B9B12F",
    "api_password": "TEST@123"
}

# Retrieve data from the API
response = requests.get(api_url, params=api_params)

# Check if the API request was successful
if response.status_code == 200:
    data = response.json()
    packet_list = data.get("packet_list")
    if not packet_list:
        print("No packet_list found in the response.")
        exit()
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
    exit()


# Step 2: Connect to your MySQL database
db_host = "203.170.73.62"
db_user = "root"
db_password = "123456"
db_name = "bifrost_erp_ideas"

# Connect to the database
db_conn = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)
db_cursor = db_conn.cursor()

# Step 3: Create a table to store the data (if not already created)
create_table_query = """
CREATE TABLE IF NOT EXISTS LeopordData_mysql (
    booking_date VARCHAR(255) NULL,
    booked_packet_cn VARCHAR(255) NULL,
    booked_packet_collect_amount VARCHAR(255) NULL,
    origin_city VARCHAR(255) NULL,
    delivery_date VARCHAR(255) NULL,
    invoice_cheque_date VARCHAR(255) NULL,
    invoice_cheque_no VARCHAR(255) NULL,
    payment_status VARCHAR(255) NULL,
    packet_charges VARCHAR(255) NULL,
    packetWeight VARCHAR(255) NULL
);
"""
db_cursor.execute(create_table_query)

# Step 4: Insert the retrieved data into the database
for row in packet_list:
    # Extract the data from the dictionary based on the packet_list element
    booking_date = row.get('booking_date')
    booked_packet_cn = row.get('booked_packet_cn')
    booked_packet_collect_amount = row.get('booked_packet_collect_amount')
    origin_city = row.get('origin_city')
    delivery_date = row.get('delivery_date')
    invoice_cheque_date = row.get('invoice_cheque_date')
    invoice_cheque_no = row.get('invoice_cheque_no')
    payment_status = row.get('payment_status')
    packet_charges = row.get('packet_charges')
    packetWeight = row.get('packetWeight')

    # SQL query to insert data into the table
    insert_query = """
    INSERT INTO LeopordData_mysql (
        booking_date,
        booked_packet_cn,
        booked_packet_collect_amount,
        origin_city,
        delivery_date,
        invoice_cheque_date,
        invoice_cheque_no,
        payment_status,
        packet_charges,
        packetWeight
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Data to be inserted into the table
    values = (
        booking_date,
        booked_packet_cn,
        booked_packet_collect_amount,
        origin_city,
        delivery_date,
        invoice_cheque_date,
        invoice_cheque_no,
        payment_status,
        packet_charges,
        packetWeight
    )

    # Execute the query and commit the changes
    db_cursor.execute(insert_query, values)
    db_conn.commit()

# Step 5: Close the database connection
db_cursor.close()
db_conn.close()
