import requests
import os
import json
import numpy as np


def get_data():
    # Data requested from Us gov website
    # Data is specified in a geojson format, and given the relevant parameters so we only get earthquake data for the UK between 2000 to 2018
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            "format": "geojson",
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )
    #Reformats the response into a python response json object
    response_json = response.json()

    #Extra info specifying file path - ONLY FOR MY PERSONAL COMPUTER (I work in a VS code workspace, where the directory initialized is not the 
    # same as the directory where this file is hence I add \Week 4\earthwuakes\earthquakes_data.json)
    file_loc = os.path.join(os.getcwd(),'Week 4','earthquakes','earthquakes_data.json')
    
    #writes data to a json file, adding indentation for ease of user usage
    with open(file_loc, 'w') as json_data_out:
        json_data_out.write(json.dumps(response_json,indent=4, sort_keys=True))
    
    #Loads the data back into Python as a Python dictionary structure
    with open(file_loc) as json_data_in:
        earthquake_data_file= json.load(json_data_in)
    
    #returns variable containing Python dictionary
    return earthquake_data_file

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return len(data["features"])


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    return earthquake["geometry"]["coordinates"][:2]


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    
    #initalise empty arrays 
    Event_mag = []
    Event_loc = []
    
    #Loop over each event within the dictionary data, and get the magnitude and locations
    #Note: this could be simplified by just including the get location and get magnitude pythons within the for loop as they only complete a single operation which isn't used again (functions most useful for structuring code and for when a operation or multiple operations needs to be completed multiple times by a script)
    for event in data["features"]:
        Event_mag.append(get_magnitude(event))
        Event_loc.append(get_location(event))
    
    #Could use a for loop or other python functions, but numpy argmax is equally valid and quick
    max_index = np.argmax(Event_mag)
    
    #return the event magnitude and location with the index of the event that had the largest magnitude
    return Event_mag[max_index], Event_loc[max_index]
        


# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)} events")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")