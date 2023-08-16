import requests
import pyodbc


from datetime import datetime, timedelta

# Calculate the date range

#end_date = datetime.now() - timedelta(days=31)
#start_date = end_date - timedelta(days=31)

# Format the dates as strings in the required format
#end_date_str = end_date.strftime("%d-%m-%Y")
#start_date_str = start_date.strftime("%d-%m-%Y")

api_url = "http://bigazure.com/api/json_v3/shipment/get_shipmentdetail.php"
headers = {"Content-Type": "application/json"}
json_data = {
    "acno": "KHI-04324",
    "usrid": "gulahmed.textile",
    "passwd": "fcV9J9jB",
    "startdate": "31-07-2023",
    "enddate": "31-07-2023"
    #"startdate": start_date_str,
    #"enddate": end_date_str
}

response = requests.post(api_url, json=json_data, headers=headers)

if response.status_code == 200:
    shipment_data = response.json()
else:
    print("API request failed with status code:", response.status_code)
    exit()

    
server = "192.168.161.250,57398"
database = "Couriers"
username = "sa"
password = "Ideas@1234"

# Establish a connection to the database
conn_str = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Iterate through the shipment data and insert into the database
for item in shipment_data:
    query = """
    INSERT INTO COURIER_BLUEX_DATA_JUNE_JULY (total_charges, dstat, cndate, ddate, bank_name, payment_method, other_charges,
    dtime, city, fps_code, stat_msg, wgt, wgt_charges, fps_date, cnno, cod_amount, paid_status, cheque_number, gst_charges)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    values = (
        item["total_charges"], item["dstat"], item["cndate"], item["ddate"], item["bank_name"], item["payment_method"],
        item["other_charges"], item["dtime"], item["city"], item["fps_code"], item["stat_msg"], item["wgt"],
        item["wgt_charges"], item["fps_date"], item["cnno"], item["cod_amount"], item["paid_status"],
        item["cheque_number"], item["gst_charges"]
    )
    cursor.execute(query, values)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data has been inserted into the database.")
