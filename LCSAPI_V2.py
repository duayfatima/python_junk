import requests
import pyodbc

# API URL
url = "http://new2.leopardscod.com/webservice/trackBookedPacketGulAhmed"
api_key = "0E33E3FB5F99FC57D18134F753B9B12F"
api_password = "TEST@123"

# Azure SQL Database connection details
server = 'aspwebappwithazuredbserver.database.windows.net'
database = 'importingExcel'
username = 'duay'
password = 'test_12345'
driver = "{ODBC Driver 17 for SQL Server}"

# Create a connection string
connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"

def get_data_from_api(url):
    params = {
        "from_date": "2023-01-01",
        "to_date": "2023-01-31",
        "api_key": api_key,
        "api_password": api_password
    }
    response = requests.get(url, params=params)
    return response.json()

def insert_data_to_sql(data):
    # Establish a connection to the Azure SQL Database
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    for item in data["packet_list"]:
        booking_date = item["booking_date"]
        booked_packet_cn = item["booked_packet_cn"]
        booked_packet_collect_amount = item["booked_packet_collect_amount"]
        origin_city = item["origin_city"]
        payment_status = item["payment_status"]
        packet_charges = item["packet_charges"]
        packet_weight = item["packetWeight"]

        for tracking_detail in item["Tracking Detail"]:
            status = tracking_detail["Status"]
            activity_date = tracking_detail["Activity_Date"]
            activity_time = tracking_detail["Activity_Time"]
            activity_datetime = tracking_detail["Activity_datetime"]

            # Insert data into the database table
            query = f"""
                INSERT INTO LeapordLCS_withPython
                (BookingDate, CNNumber, CollectAmount, OriginCity, PaymentStatus, PacketCharges, PacketWeight,
                TrackingStatus, ActivityDate, ActivityTime, ActivityDateTime)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            values = (booking_date, booked_packet_cn, booked_packet_collect_amount, origin_city, payment_status,
                      packet_charges, packet_weight, status, activity_date, activity_time, activity_datetime)

            cursor.execute(query, values)
            conn.commit()

    conn.close()

if __name__ == "__main__":
    # Get data from the API
    api_data = get_data_from_api(url)

    # Insert data into Azure SQL Database
    insert_data_to_sql(api_data)
