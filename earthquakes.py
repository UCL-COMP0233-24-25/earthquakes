# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json

def get_data():
    # Send request to the earthquake data API
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"
        }
    )

    # Parse the JSON response
    data = response.json()

    # Save the parsed data to a JSON file
    with open("earthquake_data.json", "w") as f:
        json.dump(data, f, indent=4)  # Pretty print with indent

    print("Data saved to earthquake_data.json")
    return data

# Call the function to fetch and save data



def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return len(data['features'])


def get_magnitude(earthquake):
    """Retrieve the magnitude of an earthquake item."""
    return earthquake['properties']['mag']

def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # The first two coordinates are longitude and latitude respectively
    coordinates = earthquake['geometry']['coordinates']
    latitude = coordinates[1]
    longitude = coordinates[0]
    return latitude, longitude


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    max_magnitude = -10.0  # Initialize with a very small value
    max_earthquake = None  # To store the earthquake with the highest magnitude

    # Iterate through each earthquake in the dataset
    for earthquake in data['features']:
        magnitude = get_magnitude(earthquake)  # Retrieve the magnitude

        # Check if this earthquake has a higher magnitude than the current maximum
        if magnitude > max_magnitude:
            max_magnitude = magnitude
            max_earthquake = earthquake

    # If an earthquake was found, return its magnitude and location
    if max_earthquake:
        max_location = get_location(max_earthquake)  # Get the location of the strongest earthquake
        return max_magnitude, max_location
    else:
        return None  # In case there are no earthquakes in the data


# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")