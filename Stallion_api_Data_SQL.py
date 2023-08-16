# Install required libraries if you haven't already
# You can install them using pip:
# pip install requests pyodbc
import json
import requests
import pyodbc
from datetime import datetime, timedelta

# API endpoint URL
api_url = 'https://bitrix.pk/Rest/Stallion/Get_Parcel_Position'

print ("1")
# Function to fetch data from the API using a POST request with specific dates
def fetch_data_from_api():
    from_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
    to_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')

    query_params = {
        #'FromDate': from_date,
        #'ToDate': to_date
        'FromDate': "2023-07-01",
        'ToDate': "2023-08-06"
        }

    response = requests.post(api_url, params=query_params)

    if response.status_code == 200:
        print ("2")
        return response.json()

    else:
        raise Exception(f"Failed to fetch data from API. Status Code: {response.status_code}")

# Function to connect to Azure SQL Database and insert data

'''def insert_data_into_azure_sql(data):
    server = 'aspwebappwithazuredbserver.database.windows.net'
    database = 'importingExcel'
    username = 'duay'
    password = 'test_12345'

    connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
    
    print ("3")
    
    with pyodbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            for item in data:
                query = """INSERT INTO COURIER_STALLION(Parcel_ID, Parcel_No, Courier_Name, From_City, To_City, Amount_Paid, 
                            Payment_Status, Parcel_Weight, Delivery_Charges, Delivery_Date, Payment_Date, Parcel_Status, Booking_Date)
                            
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                
                print("4")

                cursor.execute(query, item['Parcel_ID'], item['Parcel_No'], item['Courier_Name'], item['From_City'], item['To_City'], 
                               item['Amount_Paid'], item['Payment_Status'], item['Parcel_Weight'], item['Delivery_Charges'], 
                               item['Delivery_Date'], item['Payment_Date'], item['Parcel_Status'], item['Booking_Date'])'''

##############################################################################################################################################

def insert_data_into_azure_sql(data):
    '''server = 'aspwebappwithazuredbserver.database.windows.net'
    database = 'importingExcel'
    username = 'duay'
    password = 'test_12345'
    server = 'ga-pbi-1.database.windows.net'
    database = 'gapbi1'
    username = 'Umair'
    password = '@database12'''
    
    server = '192.168.161.250,57398'
    database = 'Couriers'
    username = 'sa'
    password = 'Ideas@1234'

    connection_string = (
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"Server={server};"
        f"Database={database};"
        f"Uid={username};"
        f"Pwd={password};"
    )


    #connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'

    try:
        with pyodbc.connect(connection_string) as conn:
            with conn.cursor() as cursor:
                for item in data:
                    query = """INSERT INTO Stallions_Data_WithPython(Parcel_ID, Parcel_No, Courier_Name, From_City, To_City, Amount_Paid, 
                                Payment_Status, Parcel_Weight, Delivery_Charges, Delivery_Date, Payment_Date, Parcel_Status, Booking_Date)
                                
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

                    cursor.execute(query, item['Parcel_ID'], item['Parcel_No'], item['Courier_Name'], item['From_City'], item['To_City'], 
                                   item['Amount_Paid'], item['Payment_Status'], item['Parcel_Weight'], item['Delivery_Charges'], 
                                   item['Delivery_Date'], item['Payment_Date'], item['Parcel_Status'], item['Booking_Date'])

        print("Data insertion into Azure SQL Database successful.")
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")

# Test data for demonstration purposes




if __name__ == '__main__':
    data = fetch_data_from_api()
    insert_data_into_azure_sql(data)
