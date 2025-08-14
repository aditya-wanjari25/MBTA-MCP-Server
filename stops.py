import requests
import json

url = "https://api-v3.mbta.com/stops"

payload = {}
headers = {
  'accept': 'application/vnd.api+json'
}

response = requests.request("GET", url, headers=headers, data=payload)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Save the data to a JSON file
    with open("mbta_stops.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    print("Successfully saved MBTA stops data to mbta_stops.json")

    # Filter for vehicle_type == 0 ie Tram, streetcar, light rail
    filtered = [
        item for item in data["data"]
        if item.get("attributes", {}).get("vehicle_type") == 0
    ]
    # Save to a new file
    with open("filtered_stops.json", "w") as json_file:
        json.dump(filtered, json_file, indent=4)
else:
    print(f"Error: Unable to retrieve data. Status code: {response.status_code}")
    print(response.text)