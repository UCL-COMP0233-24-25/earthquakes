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

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.

    # Read the entire content of response.txt

    # saves response in a text file
    with open('response.txt','w') as k:
        k.write(text)

    with open('response.txt', 'r') as text_file:
        content = text_file.read()

    # Parse JSON string to Python dictionary
    content_json = json.loads(content)  

    # Encodes python dictionary into a JSON file
    with open('response_json.json', 'w') as json_file:
        json.dump(content_json, json_file, indent=4)  # Ensure indentation for readability
    
    # loads JSON file
    with open('response_json.json', 'r') as json_file:
        loaded_json = json.load(json_file)
    ...

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return loaded_json 

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return data["metadata"]["count"]


def get_magnitude(loaded_json):
    """Retrive the magnitude of an earthquake item."""
    return [earthquake["properties"]["mag"] for earthquake in loaded_json["features"]]


def get_location(loaded_json,magnitude):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    for earthquake in loaded_json["features"]:
        if earthquake["properties"]["mag"] == magnitude:
            place_max_mag = earthquake["geometry"]["coordinates"][0:2]
            break
    return place_max_mag


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    max_magnitude = max(get_magnitude(data))
    location_max_magnitude = get_location(data,max_magnitude)
    return max_magnitude,location_max_magnitude
    ...


# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")