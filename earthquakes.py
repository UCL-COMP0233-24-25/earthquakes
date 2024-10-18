import requests
import json

def get_data():
    """Fetch earthquake data from the USGS web service and save it to a JSON file."""
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "1924-01-01",  # 100 years ago
            'maxlatitude': "58.723",
            'minlatitude': "50.008",
            'maxlongitude': "1.67",
            'minlongitude': "-9.756",
            'minmagnitude': "1",
            'endtime': "2024-01-01",
            'orderby': "time-asc"
        }
    )

    # Save the response text to a JSON file
    with open('earthquake_data.json', 'w') as json_file:
        json_file.write(response.text)  # Write the raw response to a file

    # Parse the JSON response to a Python dictionary
    return response.json()

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return len(data['features'])  # The number of earthquake entries

def get_magnitude(earthquake):
    """Retrieve the magnitude of an earthquake item."""
    return earthquake['properties']['mag']  # Magnitude from properties

def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    return earthquake['geometry']['coordinates'][0:2]  # First two values are latitude and longitude

def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    max_magnitude = float('-inf')  # Start with the lowest possible magnitude
    max_location = None

    for earthquake in data['features']:
        magnitude = get_magnitude(earthquake)
        if magnitude > max_magnitude:
            max_magnitude = magnitude
            max_location = get_location(earthquake)  # Update max location if a stronger quake is found

    return max_magnitude, max_location

# Main execution
if __name__ == "__main__":
    data = get_data()
    print(f"Loaded {count_earthquakes(data)} earthquakes.")
    max_magnitude, max_location = get_maximum(data)
    print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}.")
