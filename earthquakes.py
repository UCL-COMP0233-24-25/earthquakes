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
    data = response.json()
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    ...

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return data

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return data['metadata']['count']


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake['properties'].get('mag', None) #avoid keyError if mag is not exist


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    coordinates = earthquake['geometry'].get('coordinates',[])
    if len(coordinates) >= 2:
            return coordinates[0], coordinates[1]  
    else:
        return None, None


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    max_earthquake = [] 
    max_mag = float('-inf')
    max_loc = []
    for earthquake in data['features']:
        mag = get_magnitude(earthquake)
        if mag is not None:
            if mag > max_mag:
                max_mag = mag
                max_earthquake = [earthquake]
            elif mag == max_mag:
                max_earthquake.append(earthquake)

    if max_earthquake:
        for earthquake in max_earthquake:
            max_loc.append(get_location(earthquake)[:2])
        return max_mag, max_loc
    else:
        return None, None



# With all the above functions defined, we can now call them and get the result
data = get_data()
with open('xtfile.json','w',encoding='utf-8') as f:
    json.dump(data,f)
print(f"Loaded {count_earthquakes(data)}")

max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")