import requests
from datetime import datetime, timedelta
import pandas as pd

# API URL and request body
api_url = "http://bigazure.com/api/json_v3/shipment/get_shipmentdetail.php"
request_body = {
    "acno": "KHI-04324",
    "usrid": "gulahmed.textile",
    "passwd": "fcV9J9jB",
    "startdate": "",
    "enddate": ""
}

# Calculate date ranges (current day - 1 to 30 days back)
end_date = datetime.now() - timedelta(days=1)
start_date = datetime.now() - timedelta(days=5)

# Format dates as required ("dd-mm-yyyy")
start_date_str = start_date.strftime("%d-%m-%Y")
end_date_str = end_date.strftime("%d-%m-%Y")

# Update the request body with new date ranges
request_body["startdate"] = start_date_str
request_body["enddate"] = end_date_str

# Make the API request
response = requests.post(api_url, json=request_body)

# Initialize an empty list to store transformed data
data_list = []

# Check if the request was successful
if response.status_code == 200:
    api_data = response.json()
    # Process the API response (api_data) and transform it into tabular format
    for item in api_data:
        fps_date_str = item["fps_date"]
        
        if fps_date_str != "None":  # Check if fps_date_str is not "None"
            
            fps_date = datetime.strptime(fps_date_str, "%Y-%m-%d %H:%M:%S")
            data_list.append({ "fps_date": fps_date })
        else:
            data_list.append({ "fps_date": item["fps_date"]})
        
    #Create a DataFrame from the transformed data
    df = pd.DataFrame(data_list)
    print(df)

    # Convert the DataFrame to a JSON string
    #result_json = df.to_json(orient="records")
    #print(result_json)
else:
    print("not found")
