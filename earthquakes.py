# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json
import numpy as np

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
            "endtime": "2024-10-20",
            "orderby": "time-asc"}
    )

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    data = json.loads(text)
    with open('response.json','w') as f:
        json.dump(data,f)
    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return data

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    earthquake_times = data['metadata']['count']
    return earthquake_times


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    mag_list=[]
    for item in earthquake:
        mag_list.append(item['properties']['mag'])
    return mag_list


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    loc_list=[]
    for item in earthquake:
        loc_list.append(item['geometry']['coordinates'][:2])
    return loc_list


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    earthquake = data['features']
    max_mag = np.max([get_magnitude(earthquake)])
    max_indices = [i for i, value in enumerate(get_magnitude(earthquake)) if value == max_mag]
    if len(max_indices) == 1:
        max_loc = get_location(earthquake)[max_indices[0]]
    else:
        max_loc = []
        for index in max_indices:
            max_loc.append(get_location(earthquake)[index])
    return max_mag, max_loc



# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")