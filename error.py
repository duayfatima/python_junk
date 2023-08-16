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
        data_list.append({
            "Total Charges": item["total_charges"],
            "Status": item["dstat"],
            "Creation Date": item["cndate"],
            "Delivery Date": item["ddate"],
            "Bank Name": item["bank_name"],
            "Payment Method": item["payment_method"],
            "Other Charges": item["other_charges"],
            "Time": item["dtime"],
            "City": item["city"],
            "FPS Code": item["fps_code"],
            "Status Message": item["stat_msg"],
            "Weight": item["wgt"],
            "Weight Charges": item["wgt_charges"],
            "FPS Date": item["fps_date"],
            "CN No": item["cnno"],
            "COD Amount": item["cod_amount"],
            "Paid Status": item["paid_status"],
            "Cheque Number": item["cheque_number"],
            "GST Charges": item["gst_charges"]
        })

    # Create a DataFrame from the transformed data
    df = pd.DataFrame(data_list)
    print(df)

    # Convert the DataFrame to a JSON string
    result_json = df.to_json(orient="records")
else:
    result_json = []

result_json
