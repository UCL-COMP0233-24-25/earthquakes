# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json


def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
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
            "orderby": "time-asc"}
    )

    # Ensure the response is successful  
    if response.status_code == 200:
        return response.json()  # Ensure this returns the parsed JSON  
    else:
        print(f"Error fetching data: {response.status_code}")
        return {}  # Return an empty dict if there's an error

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return response.json

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return len(data['features'])


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake['properties']['mag']


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    coords = earthquake['geometry']['coordinates']
    return (coords[1], coords[0])  # Return (latitude, longitude)
def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    if 'features' in data and len(data['features']) > 0:
        max_earthquake = max(data['features'], key=get_magnitude)  # Find the strongest earthquake  
        return get_magnitude(max_earthquake), get_location(max_earthquake)  # Return magnitude and location  
    return None, None  # If no earthquakes exist

# With all the above functions defined, we can now call them and get the result  
data = get_data()

# Make sure data is loaded correctly  
if isinstance(data, dict) and 'features' in data:
    print(f"Loaded {count_earthquakes(data)} earthquakes.")
    max_magnitude, max_location = get_maximum(data)

    if max_magnitude is not None:
        print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")
    else:
        print("No earthquake data available.")
else:
    print("Failed to load earthquake data.")