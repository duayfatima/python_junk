# Install required libraries if you haven't already
# You can install them using pip:
# pip install requests pyodbc

import requests
import pyodbc
from datetime import datetime, timedelta

# API endpoint URL
api_url = 'https://v9.footfallcam.com/FootfallCam/exportData'

# Function to fetch data from the API using a GET request with specific dates
def fetch_data_from_api():
    from_date = (datetime.utcnow() - timedelta(days=1)).strftime('%d/%m/%Y')
    to_date = (datetime.utcnow() - timedelta(days=1)).strftime('%d/%m/%Y')
    #from_date='01/07/2023'
    #to_date='23/07/2023'

    query_params = {
        'infoJson': f'{{"cat":"1","id":["26509"],"data":[],"fromdate":"{from_date}","todate":"{to_date}","period":"0","dateformat":"dd/MM/yyyy","timeformat":"HH:mm:ss"}}',
        'access_token': '480030004500680041006C00640055003300420047004E006F004C00640044005A0056004300710058006D006B0058003100740073005500520042006F006600620052006E003200710033004900560058004F00610079006E007800370069004D00370052004D00740032006800620051004E0059004B007400440031006B0045007A005A00730070004F00340041006F006B0046004F0059004900320059007500410062006C0072006D004C0034006C004300550074006400570074006C0048007300380035005A006D004F00710036004800410031007100760065006F0061006100340077006C004C0030004900320050006A00590042006C006E004B0053004D004200500076006C00590076006D004900310069004F002F006C00440077004F006B007900440031005600740035006A007A00500048003200350057004A004F007000380054005300300064003600460057006500370076004D004500460065006500750039006800490061007300480031003900610068004D00690036005400570038006400330038004B006E0078006400730074002F0043004B004200560079005400350043006B00550044006D004C005800670057006800580044004F00780052006B00430031005A0039006C006300450030004900540077004A00760030006300320072002B00470058004200420073006E0069004F00770034006D006F006F005500770036004D0061004A0041004C00570071004C004F00710068006E006500490039004A005100420042002B00690047004300550079004E005200660046004900540059006D0056003800740037004700440033004C0063002B0062006B00720079007800350041004C0046004D0057004B00630052007A006200720069004A004A006F004B007300390069005200530057005200590043007000790066004200630054004F0030005900750031006D007900770067006C006D004C0059007400450050002F00540047002F0077006200700063005300680074006600530046006D0047005500650067004B00310032005300470038006B006C00530062004A004700540033004F00510050007A00360042005400680073006D004F007000500079006B0055003500690041004B005300360068006C00530058006D0072004E00640041007400440041007900430048007300530056006A00470036004B00650062004100390071004200420033004D006A007A006500610043004A00730051004E0051006E0074002B00590067006D00350035006C0064004300560038005300670048002F004A00660048006C007500690043004C0036006600720072007A0046003100790058007900670061004300520072006B0041006C0068006C0073004F0054004C005A006300740046006B0052006600570079005900450033006700610079006400570036005A00360036006B00560052006F003900750033005900580068002F0066006900360056004F00590036003200720069007600790056005200680042002B00710057002B004A0031004800420034005200360077006A0038006900490070004A005A0037004C00770078004900320037002B00710030006C00790072006D0073002F004D0043004D00530031006E00370075004C00470069005400680055005400320076005100380051006E00590036007700670051004F0078006A0057006C0041003D00'}
    response = requests.get(api_url, params=query_params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from API. Status Code: {response.status_code}")

# Function to connect to Azure SQL Database and insert data

def insert_data_into_azure_sql(data):
    
        # Your Azure SQL Database connection parameters
    server = 'hmz-pbi.database.windows.net'
    database = 'hmz-pbi-prod2'
    username = 'hmzpbiadmin'
    password = '@hmzpbi123'
    connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'

    try:
        with pyodbc.connect(connection_string) as conn:
            with conn.cursor() as cursor:
                for item in data['Data']:
                    query = """INSERT INTO SHARJAH_API_DATA(
                        AvgVisitDuration,
                        NewCustomer,
                        ReturningCustomer,
                        LessThanFifteen,
                        LessThanThirty,
                        OverThirty,
                        ReturnInWeek,
                        AggregationStatus,
                        ZoneID,
                        Week,
                        WeekString,
                        Month,
                        SiteTags,
                        SiteTagsCount,
                        Day,
                        TransactionCount,
                        SalesAmount,
                        AvgTransactionValue,
                        Company,
                        Site,
                        Counter,
                        DateTime,
                        ValueDateTime,
                        DateTimeFormat,
                        ValueIn,
                        ValueOut,
                        OutsideTraffic,
                        TurnInRate,
                        SalesConversion,
                        VerificationStatus,
                        BranchId,
                        branchCode,
                        Longitude,
                        Latitude,
                        CameraSerial,
                        CameraId,
                        CoverageDays,
                        StartOfDate,
                        ReturningRate
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

                    cursor.execute(
                        query,
                        item['AvgVisitDuration'],
                        item['NewCustomer'],
                        item['ReturningCustomer'],
                        item['LessThanFifteen'],
                        item['LessThanThirty'],
                        item['OverThirty'],
                        item['ReturnInWeek'],
                        item['AggregationStatus'],
                        item['ZoneID'],
                        item['Week'],
                        item['WeekString'],
                        item['Month'],
                        item['SiteTags'],
                        item['SiteTagsCount'],
                        item['Day'],
                        item['TransactionCount'],
                        item['SalesAmount'],
                        item['AvgTransactionValue'],
                        item['Company'],
                        item['Site'],
                        item['Counter'],
                        item['DateTime'],
                        item['ValueDateTime'],
                        item['DateTimeFormat'],
                        item['ValueIn'],
                        item['ValueOut'],
                        item['OutsideTraffic'],
                        item['TurnInRate'],
                        item['SalesConversion'],
                        item['VerificationStatus'],
                        item['BranchId'],
                        item['branchCode'],
                        item['Longitude'],
                        item['Latitude'],
                        item['CameraSerial'],
                        item['CameraId'],
                        item['CoverageDays'],
                        item['StartOfDate'],
                        item['ReturningRate']
                    )

        print("Data insertion into Azure SQL Database successful.")
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")

def main():
    # Fetch data from the API
    data = fetch_data_from_api()

    # Insert data into Azure SQL Database
    insert_data_into_azure_sql(data)

if __name__ == "__main__":
    main()
