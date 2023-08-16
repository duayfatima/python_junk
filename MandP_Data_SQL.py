import requests
import json
import pyodbc
from datetime import datetime, timedelta

from_date = (datetime.now()- timedelta(days=1)).strftime('%Y-%m-%dT00:00:00.000Z')
to_date = (datetime.now()- timedelta(days=1)).strftime('%Y-%m-%dT23:59:59.999Z')

def main():
    # API URL
    api_url = "https://mnpcourier.com/mycodapi/api/Reports/Payment_Report_Detail_CNWise_GulAhmed"

    # Request data (update with your actual username, password, and other parameters)
    request_data = {
        "UserName": "UMAIR_4G132",
        "Password": "AbcD@1234",
        "dateFrom": "2023-07-01T00:00:00.000Z",
        "dateTo": "2023-08-01T23:59:59.999Z",
        #"dateFrom": "2023-07-25T00:00:00.000Z",
        #"dateTo": "2023-07-26T00:00:00.000Z",
        #"dateFrom": from_date,
        #"dateTo": to_date,
        "AccountNumber": "4G132",
        "locationID": ""
    }

    try:
        # Make the POST request to the API
        response = requests.post(api_url, json=request_data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            json_data = response.json()
            #print(json_data)

            # Connect to your local SQL Server database
            '''server = "(localdb)\\MyLocalDB"  # Replace with your SQL Server instance name
            database = "DataFromAPI"  # Replace with your database name
            conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
            #conn_str = 'DRIVER={SQL Server};SERVER=(localdb)\MyLocalDB;DATABASE=DataFromAPI;Trusted_Connection=yes;'''

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
            connection = pyodbc.connect(conn_str)
            cursor = connection.cursor()

            # Assuming 'data_table' is the name of the table in your database
            # Adjust column names and data types as per your table structure
            for item in json_data[0]['Data']:
                query = ("INSERT INTO MandP_Data_withPython (consignmentNumber, clientname, BookingDate, consignee, pcs, SERVICE, name, WEIGHT, pieces, serviceTypeName, orderRefNo, deliveryDate, receivedBy, ReceiptAmount, DESTINATION, RRSTATUS, RRPayable, CNApproved, paidon, PaymentMode, LocationName) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);")
                cursor.execute(query, (
                    item['consignmentNumber'],
                    item['clientname'],
                    item['BookingDate'],
                    item['consignee'],
                    item['pcs'],
                    item['SERVICE'],
                    item['name'],
                    item['WEIGHT'],
                    item['pieces'],
                    item['serviceTypeName'],
                    item['orderRefNo'],
                    item['deliveryDate'],
                    item['receivedBy'],
                    item['ReceiptAmount'],
                    item['DESTINATION'],
                    item['RRSTATUS'],
                    item['RRPayable'],
                    item['CNApproved'],
                    item['paidon'],
                    item['PaymentMode'],
                    item['LocationName']
                ))


            # Commit the changes and close the connection
            connection.commit()
            connection.close()

            print("Data has been successfully inserted into the database.")
        else:
            print(f"Error: API returned status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
