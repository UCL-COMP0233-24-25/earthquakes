# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
# 10pm

import json


def get_data():
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            "starttime": "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc",
        },
    )

    text = response.text
    jsonText = json.loads(text)

    return jsonText


def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return len(data["features"])


def get_magnitude(earthquake):
    return earthquake["properties"]["mag"]


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    one = earthquake["geometry"]["coordinates"][1]
    two = earthquake["geometry"]["coordinates"][0]
    return one, two


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    max_magnitude = 0.0
    max_earthquakes = None

    for earthquake in data["features"]:
        if get_magnitude(earthquake) > max_magnitude:
            max_magnitude = get_magnitude(earthquake)
            max_earthquakes = earthquake

    return max_magnitude, get_location(max_earthquakes)


# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")
