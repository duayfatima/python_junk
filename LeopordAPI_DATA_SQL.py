import requests
import pyodbc
import json
from datetime import datetime, timedelta

from_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
to_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
   
# API URL
api_url = "http://new2.leopardscod.com/webservice/trackBookedPacketGulAhmed"
api_params = {
    "from_date": from_date,
    "to_date": to_date,
    #"from_date": "2023-06-26",
    #"to_date": "2023-07-24",
    "api_key": "0E33E3FB5F99FC57D18134F753B9B12F",
    "api_password": "TEST@123"
}

# Retrieve data from the API
response = requests.get(api_url, params=api_params)

# Check if the API request was successful
if response.status_code == 200:
    data = response.json()
    packet_list = data.get("packet_list", [])

    # Connect to Azure SQL Database
    '''server = 'aspwebappwithazuredbserver.database.windows.net'
    database = 'importingExcel'
    username = 'duay'
    password = 'test_12345'''
    server = '192.168.161.250,57398'
    database = 'Couriers'
    username = 'sa'
    password = 'Ideas@1234'

    conn_str = (
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"Server={server};"
        f"Database={database};"
        f"Uid={username};"
        f"Pwd={password};"
    )

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Create a table to store the data (if it doesn't exist already)

    # Insert data into the table
    
    for packet in packet_list:
        booking_date = packet.get("booking_date", "")
        booked_packet_cn = packet.get("booked_packet_cn", "")
        booked_packet_collect_amount = packet.get("booked_packet_collect_amount", "")
        origin_city = packet.get("origin_city", "")
        delivery_date = packet.get("delivery_date", "")
        invoice_cheque_date = packet.get("invoice_cheque_date", "")
        invoice_cheque_no = packet.get("invoice_cheque_no", "")
        payment_status = packet.get("payment_status", "")
        packet_charges = packet.get("packet_charges", "")
        packetWeight = packet.get("packetWeight", "")

        insert_query = """
            INSERT INTO LeapordLCS_withPython 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        cursor.execute(insert_query, (
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
        ))
        conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    print("Data successfully retrieved and stored in Azure SQL Database.")
else:
    print(f"Failed to retrieve data from the API. Status code: {response.status_code}")
