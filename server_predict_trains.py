from mcp.server.fastmcp import FastMCP
import json, pytz, requests



# Initialize MCP Server
mcp = FastMCP("MBTA-Predict-Next-Train")
TZ = pytz.timezone("America/New_York")


# Helper Functions
def get_station_details(station_name: str, file_path: str = "filtered_stops.json") -> list:
    """
    Gets platform IDs and names for a specified station from a JSON file.

    Args:
        station_name (str): The name of the station to search for. T
        file_path (str, optional): The path to the JSON file containing station data. 

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents
                    a platform and contains its 'id' and 'platform_name'.
                    Example: `[{'id': 'stop_id_1', 'platform_name': 'Platform A'}, ...]`

    """
    with open(file_path, "r") as f:
        data = json.load(f)

    return [
        {"id": item["id"], "platform_name": item.get("attributes", {}).get("platform_name", "Unknown")}
        for item in data
        if item.get("attributes", {}).get("name", "").lower() == station_name.lower()
    ]

from datetime import datetime

def format_time(dt: datetime) -> str:
    """
    Formats a datetime object into a 'H:MM AM/PM' string without a leading zero on the hour.

    Args:
        dt (datetime): The datetime object to be formatted.

    Returns:
        str: A string representing the local time in the format 'H:MM AM/PM'.
             Example: "9:26 PM", "1:00 AM", "12:30 PM".
    """
    return dt.strftime("%I:%M %p").lstrip("0")


def get_predictions_for_stop(stop_id: str) -> list[tuple[int, str]]:
    """
    Retrieves and formats the next two arrival predictions for a given MBTA stop.

    Args:
        stop_id (str): The unique identifier for the MBTA stop.

    Returns:
        list[tuple[int, str]]: A list of tuples, where each tuple contains:
                               - An integer representing the number of minutes until arrival.
                               - A string representing the formatted local arrival time (e.g., '9:26 PM').
                               The list will contain up to two predictions, sorted by soonest arrival.

    """
    
    url = f"https://api-v3.mbta.com/predictions?filter[stop]={stop_id}"
    headers = {"accept": "application/vnd.api+json"}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
    payload = resp.json()

    now = datetime.now(TZ)
    results: list[tuple[int, str]] = []

    for item in payload.get("data", []):
        arrival_str = item.get("attributes", {}).get("arrival_time")
        if not arrival_str:
            continue
        try:
            # Parse API time (has timezone offset), convert to local
            arrival_dt = datetime.fromisoformat(arrival_str).astimezone(TZ)
        except ValueError: # More specific exception for parsing issues
            continue

        mins = int((arrival_dt - now).total_seconds() // 60)
        if mins >= 0: # Only include predictions that are in the future or current minute
            results.append((mins, format_time(arrival_dt)))

    # Sort by soonest and keep up to the next two
    results.sort(key=lambda x: x[0])
    return results[:2]

def humanize_predictions(platform_name: str, preds: list[tuple[int, str]]) -> str:
    if not preds:
        return f"No upcoming trains to {platform_name}."
    parts = []
    for mins, when in preds:
        if mins == 0:
            parts.append(f"due at {when}")
        elif mins == 1:
            parts.append(f"in 1 min at {when}")
        else:
            parts.append(f"in {mins} mins at {when}")
    # Join first and second prediction with ' and '
    return f"Train to {platform_name} is " + " and ".join(parts) + "."

@mcp.tool()
def get_next_trains_for_station(station_name: str) -> str:
    """
    Fetches and formats next train arrival predictions for all platforms at a given MBTA station.

    This function first identifies all platform IDs associated with the specified
    `station_name`. For each platform, it retrieves up to the next two train
    arrival predictions and then formats these predictions into a human-readable
    sentence. The results for each platform (direction) are concatenated to
    provide a comprehensive overview of upcoming trains at the station.

    Args:
        station_name (str): The name of the transit station (e.g., 'Fenway')
                            for which to retrieve train predictions.

    Returns:
        str: A formatted string summarizing the next train arrivals for each
             platform/direction at the station. If no platforms are found,
             it returns a message indicating that.
             Example: 'Train to Inbound is in 2 mins at 9:26 PM and in 12 mins at 9:36 PM;
                       Train to Outbound is in 5 mins at 9:29 PM and in 15 mins at 9:39 PM.'
    """
    platforms = get_station_details(station_name)
    if not platforms:
        return f"No platforms found for station '{station_name}'."

    lines = []
    for p in platforms:
        preds = get_predictions_for_stop(p["id"])
        # Ensure 'platform_name' exists, default to 'Unknown' if not.
        lines.append(humanize_predictions(p.get("platform_name") or "Unknown", preds))

    # Separate the two directions with '; ' for readability
    return "; ".join(lines) 


if __name__ == "__main__":
    mcp.run(transport = "stdio")
