# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json

def get_data():
    # With requests, we can ask the web service for the data.
    # We have a set of parameters to limit our search to certain dates and locations and at least of magnitude 1(almost 19 years and Britain)
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
    earthquake_text = response.text
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    ...
    with open('earthquake.json', 'w') as f:
        f.write(earthquake_text)
    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return

with open('earthquake.json', 'r') as f:
     earthquake_info = f.read()

data = json.loads(earthquake_info) # used json to convert data into a dictionary then my functions are easy to work with 


def count_earthquakes(data):
    x = len(data["features"])
    return x


def get_magnitude(earthquake):
    x = earthquake["properties"]["mag"]
    return x



def get_location(earthquake):
    x = earthquake["geometry"]["coordinates"]
    y = x[:2]
    # There are 3 coordinates, but we don't care about the third (altitude)
    return y


def get_maximum(data):
    z=0
    x=[0,0]
    for i in range(count_earthquakes(data)):
        if get_magnitude(data["features"][i])>z:
            z=get_magnitude(data["features"][i])
            x=get_location(data["features"][i])
    return z,x

    ...


# With all the above functions defined, we can now call them and get the result

print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")