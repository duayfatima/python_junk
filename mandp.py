import requests
import json
import pyodbc
from datetime import datetime, timedelta

def get_yesterday():
    today = datetime.today()
    yesterday = today - timedelta(days=4)
    return yesterday.strftime('%Y-%m-%dT00:00:00.000Z'), yesterday.strftime('%Y-%m-%dT23:59:59.999Z')

def main():
    # API URL
    api_url = "https://mnpcourier.com/mycodapi/api/Reports/Payment_Report_Detail_CNWise_GulAhmed"

    # Request data for yesterday's date
    date_from, date_to = get_yesterday()
    request_data = {
        "UserName": "UMAIR_4G132",
        "Password": "AbcD@1234",
        "dateFrom": date_from,
        "dateTo": date_to,
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

            # Connect to your local SQL Server database
            server = "(localdb)\\MyLocalDB"  # Replace with your SQL Server instance name
            database = "DataFromAPI"  # Replace with your database name
            conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
            connection = pyodbc.connect(conn_str)
            cursor = connection.cursor()

            # Assuming 'data_table' is the name of the table in your database
            # Adjust column names and data types as per your table structure
            for item in json_data[0]['Data']:
                query = "INSERT INTO DataFromMandP (consignmentNumber, clientname, BookingDate, consignee, pcs, SERVICE, name, WEIGHT, pieces, serviceTypeName, orderRefNo, ReceiptAmount, DESTINATION, RRPayable, CNApproved, PaymentMode, LocationName) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
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
                    item['ReceiptAmount'],
                    item['DESTINATION'],
                    item['RRPayable'],
                    item['CNApproved'],
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
