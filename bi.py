import requests
from datetime import datetime, timedelta, date

# Calculate date ranges
current_date = date.today()
from_date = current_date - timedelta(days=1)
to_date = current_date - timedelta(days=90)

# Convert dates to string format (YYYY-MM-DD)
from_date_str = from_date.strftime('%Y-%m-%d')
to_date_str = to_date.strftime('%Y-%m-%d')

# API URL
api_url = "http://new2.leopardscod.com/webservice/trackBookedPacketGulAhmed"
api_params = {
    "from_date": from_date_str,
    "to_date": to_date_str,
    "api_key": "0E33E3FB5F99FC57D18134F753B9B12F",
    "api_password": "TEST@123"
}

try:
    # Retrieve data from the API
    response = requests.get(api_url, params=api_params)

    # Check if the API request was successful
    if response.status_code == 200:
        try:
            data = response.json()
            packet_list = data.get("packet_list", [])
            print(packet_list)
        except ValueError as ve:
            print("Error: Unable to parse response as JSON.")
    else:
        print(f"Failed to retrieve data from the API. Status code: {response.status_code}")
     
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
