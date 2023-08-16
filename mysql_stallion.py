import requests
import mysql.connector
import json
from datetime import datetime, timedelta


# Step 1: Make the API request and get the data

fromDate = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
toDate = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')


api_url = "https://bitrix.pk/Rest/Stallion/Get_Parcel_Position"
api_params = {
    #"FromDate": "2023-01-01",
    #"ToDate": "2023-01-05"
    "FromDate": fromDate,
    "ToDate": toDate
}

response = requests.post(api_url, json=api_params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
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
CREATE TABLE IF NOT EXISTS STALLION_DATA_mysql (
    Parcel_ID VARCHAR(255),
    Parcel_No VARCHAR(255),
    Courier_Name VARCHAR(255),
    From_City VARCHAR(255),
    To_City VARCHAR(255),
    Amount_Paid VARCHAR(255),
    Payment_Status VARCHAR(255),
    Parcel_Weight VARCHAR(255),
    Delivery_Charges VARCHAR(255),
    Delivery_Date VARCHAR(255),
    Payment_Date VARCHAR(255),
    Parcel_Status VARCHAR(255),
    Booking_Date VARCHAR(255)
);
"""
db_cursor.execute(create_table_query)

# Step 4: Insert the retrieved data into the database
for row in data:
    # Extract the data from the dictionary based on the API response structure
    parcel_id = row.get('Parcel_ID')
    parcel_no = row.get('Parcel_No')
    courier_name = row.get('Courier_Name')
    from_city = row.get('From_City')
    to_city = row.get('To_City')
    amount_paid = row.get('Amount_Paid')
    payment_status = row.get('Payment_Status')
    parcel_weight = row.get('Parcel_Weight')
    delivery_charges = row.get('Delivery_Charges')
    delivery_date = row.get('Delivery_Date')
    payment_date = row.get('Payment_Date')
    parcel_status = row.get('Parcel_Status')
    booking_date = row.get('Booking_Date')

    # SQL query to insert data into the table
    insert_query = """
    INSERT INTO STALLION_DATA_mysql (
        Parcel_ID,
        Parcel_No,
        Courier_Name,
        From_City,
        To_City,
        Amount_Paid,
        Payment_Status,
        Parcel_Weight,
        Delivery_Charges,
        Delivery_Date,
        Payment_Date,
        Parcel_Status,
        Booking_Date
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Data to be inserted into the table
    values = (
        parcel_id,
        parcel_no,
        courier_name,
        from_city,
        to_city,
        amount_paid,
        payment_status,
        parcel_weight,
        delivery_charges,
        delivery_date,
        payment_date,
        parcel_status,
        booking_date
    )

    # Execute the query and commit the changes
    db_cursor.execute(insert_query, values)
    db_conn.commit()

# Step 5: Close the database connection
db_cursor.close()
db_conn.close()
