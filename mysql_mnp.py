import requests
import mysql.connector
import json
from datetime import datetime, timedelta


def get_yesterday():
    today = datetime.today()
    yesterday = today - timedelta(days=4)
    return yesterday.strftime('%Y-%m-%dT00:00:00.000Z'), yesterday.strftime('%Y-%m-%dT23:59:59.999Z')
# Step 1: Make the API request and get the data

api_url = "https://mnpcourier.com/mycodapi/api/Reports/Payment_Report_Detail_CNWise_GulAhmed"
date_from, date_to = get_yesterday()
api_body = {
    "UserName": "UMAIR_4G132",
    "Password": "AbcD@1234",
    "dateFrom":date_from,
    "dateTo":date_to,
    #"dateFrom": "2023-01-01T00:00:00.000Z",
    #"dateTo": "2023-01-31T23:59:59.999Z",
    "AccountNumber": "4G132",
    "locationID": ""
}

response = requests.post(api_url, json=api_body)

# Check if the request was successful
if response.status_code == 200:
    json_data = response.json()
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
create_table_query = """CREATE TABLE IF NOT EXISTS MandP_DATA_mysql (
    consignmentNumber VARCHAR(255),
    clientname VARCHAR(255),
    BookingDate VARCHAR(255),
    consignee VARCHAR(255),
    pcs VARCHAR(255),
    SERVICE VARCHAR(255),
    name VARCHAR(255),
    WEIGHT VARCHAR(255),
    pieces VARCHAR(255),
    serviceTypeName VARCHAR(255),
    orderRefNo VARCHAR(255),
    deliveryDate VARCHAR(255),
    receivedBy VARCHAR(255),
    ReceiptAmount VARCHAR(255),
    DESTINATION VARCHAR(255),
    RRSTATUS VARCHAR(255),
    RRPayable VARCHAR(255),
    CNApproved VARCHAR(255),
    paidon VARCHAR(255),
    PaymentMode VARCHAR(255),
    LocationName VARCHAR(255)
);

"""
db_cursor.execute(create_table_query)

# Step 4: Insert the retrieved data into the database
for row in json_data[0]['Data']:
    # SQL query to insert data into the table
    insert_query = """
    INSERT INTO MandP_DATA_mysql (
        consignmentNumber,
        clientname,
        BookingDate,
        consignee,
        pcs,
        SERVICE,
        name,
        WEIGHT,
        pieces,
        serviceTypeName,
        orderRefNo,
        deliveryDate,
        receivedBy,
        ReceiptAmount,
        DESTINATION,
        RRSTATUS,
        RRPayable,
        CNApproved,
        paidon,
        PaymentMode,
        LocationName
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Data to be inserted into the table
    values = (
        row.get("consignmentNumber"),
        row.get("clientname"),
        row.get("BookingDate"),
        row.get("consignee"),
        row.get("pcs"),
        row.get("SERVICE"),
        row.get("name"),
        row.get("WEIGHT"),
        row.get("pieces"),
        row.get("serviceTypeName"),
        row.get("orderRefNo"),
        row.get("deliveryDate"),
        row.get("receivedBy"),
        row.get("ReceiptAmount"),
        row.get("DESTINATION"),
        row.get("RRSTATUS"),
        row.get("RRPayable"),
        row.get("CNApproved"),
        row.get("paidon"),
        row.get("PaymentMode"),
        row.get("LocationName")
    )

    # Execute the query and commit the changes
    db_cursor.execute(insert_query, values)
    db_conn.commit()


# Step 5: Close the database connection
db_cursor.close()
db_conn.close()
