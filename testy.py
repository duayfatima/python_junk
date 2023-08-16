import requests
import json
from datetime import datetime, timedelta
import pandas as pd

# Calculate date ranges
current_date = datetime.now()
date_to = current_date - timedelta(days=1)
date_from = current_date - timedelta(days=90)

# Construct the modified request body
request_body = {
    "UserName": "UMAIR_4G132",
    "Password": "AbcD@1234",
    "dateFrom": date_from.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
    "dateTo": date_to.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
    "AccountNumber": "4G132",
    "locationID": ""
}

# Convert the request body to JSON format
json_data = json.dumps(request_body)

# Make the POST request
url = "https://mnpcourier.com/mycodapi/api/Reports/Payment_Report_Detail_CNWise_GulAhmed"
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, data=json_data, headers=headers)

# Process the API response as needed
if response.status_code == 200:
    api_response = response.json()
    
    # Loop through the list of dictionaries and extract the "Data" field from each
    data_list = [entry["Data"] for entry in api_response]
    
    # Combine the "Data" lists into a single list
    combined_data = []
    for data in data_list:
        combined_data.extend(data)
    
    # Convert the combined "Data" list into a DataFrame
    MandP = pd.DataFrame(combined_data)
    
    # Print the DataFrame
    print(MandP)
else:
    print("Error:", response.status_code)
    print(response.text)
