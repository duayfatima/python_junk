import requests
import pyodbc
from datetime import datetime, timedelta

# API endpoint URL
api_url = 'http://new2.leopardscod.com/webservice/trackBookedPacketGulAhmed'

# Function to fetch data from the API using a GET request with specific dates
def fetch_data_from_api():
    #from_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
    #to_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')

    api_key = '0E33E3FB5F99FC57D18134F753B9B12F'
    api_password = 'TEST@123'

    query_params = {
        #'from_date': from_date,
        #'to_date': to_date,
        'from_date': "2023-01-01",
        'to_date': "2023-01-01",
        'api_key': api_key,
        'api_password': api_password
    }

    response = requests.get(api_url, params=query_params)

    if response.status_code == 200:
        print("1")
        return response.json().get('packet_list', [])

    else:
        raise Exception(f"Failed to fetch data from API. Status Code: {response.status_code}")
################################################################################


#######################################################################################33



def insert_data_into_azure_sql(data):
    server = 'aspwebappwithazuredbserver.database.windows.net'
    database = 'importingExcel'
    username = 'duay'
    password = 'test_12345'

    connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
    print("2")

    try:
        with pyodbc.connect(connection_string) as conn:
            with conn.cursor() as cursor:
                for item in data:
                    query = """INSERT INTO LeapordLCS_withPython(booking_date, booked_packet_cn, booked_packet_collect_amount, origin_city,
                                   delivery_date, invoice_cheque_date, invoice_cheque_no, payment_status,
                                   packet_charges, packetWeight)
                                
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

                    #booking_date_str = item.get('booking_date')
                    #Convert the API date string to a Python datetime object
                    #booking_date = datetime.strptime(booking_date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
                    '''booking_date = item.get('booking_date')
                    booked_packet_cn = item.get('booked_packet_cn')
                    booked_packet_collect_amount = item.get('booked_packet_collect_amount')
                    origin_city = item.get('origin_city')
                    delivery_date = item.get('delivery_date')
                    invoice_cheque_date = item.get('invoice_cheque_date')
                    invoice_cheque_no = item.get('invoice_cheque_no')
                    payment_status = item.get('payment_status')
                    packet_charges = item.get('packet_charges')
                    packetWeight = item.get('packetWeight')'''

                    cursor.execute(query, booking_date['booking_date'], booked_packet_cn['booked_packet_cn'], booked_packet_collect_amount['booked_packet_collect_amount'], origin_city['origin_city'],
                                   delivery_date['delivery_date'], invoice_cheque_date['invoice_cheque_date'], invoice_cheque_no['invoice_cheque_no'], payment_status['payment_status'],
                                   packet_charges['packet_charges'], packetWeight['packetWeight'])

                    
                    '''cursor.execute(query, booking_date, booked_packet_cn, booked_packet_collect_amount, origin_city,
                                   delivery_date, invoice_cheque_date, invoice_cheque_no, payment_status,
                                   packet_charges, packetWeight)'''

        print("Data insertion into Azure SQL Database successful.")
        
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")


if __name__ == '__main__':
    data = fetch_data_from_api()
    insert_data_into_azure_sql(data)
