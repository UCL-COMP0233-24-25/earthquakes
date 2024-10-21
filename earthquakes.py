import numpy as np
import requests        # powerful library for communicating over the internet
import json
import datetime


def get_data():
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

    # get json format
    data = response.json()

    return data



def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    # Extract number from metadata
    meta_count = data['metadata']['count']

    # Extractnumber from counting features
    feature_count = len(data['features'])

    if meta_count == feature_count:
        return meta_count
    else:
        print('Discrepency between metadata count vlue and number of features. Using number of features as the value.')
        return feature_count
    



def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    magnitude = earthquake['properties']['mag']
    return magnitude


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    lat, long, _ = earthquake['geometry']['coordinates']
    return [lat, long]

def get_location_description(earthquake):
    """Retrieve the description of the location of an earthquake item."""
    description = earthquake['properties']['place']
    return description

def get_time(earthquake):
    """Retrieve the time of an eartquake. Convert from Unix Timestamp"""
    unix_time_ms = earthquake['properties']['time']
    time_sec = unix_time_ms / 1000 # convert from miliseconds to seconds
    date_time = datetime.datetime.utcfromtimestamp(time_sec)  # Convert to a datetime object in UTC
    return date_time

def get_earthquake_id(earthquake):
    """Retrieve id for earthqauke"""
    id = earthquake['id']
    return id

def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data. 
    Checks for multiple quakes of same magnitude """
    max_mag = 0
    earthquakes ={}

    for earthquake in data['features']:
        mag = get_magnitude(earthquake)
        if mag > max_mag:
            # re-empty dict 
            earthquakes ={}
            max_id = get_earthquake_id(earthquake)
            max_mag = mag
            max_loc = get_location(earthquake)
            max_loc_description =get_location_description(earthquake)
            max_time = get_time(earthquake)
            earthquakes[max_id] ={}
            earthquakes[max_id]['Magnitude'] = max_mag
            earthquakes[max_id]['Location'] = max_loc
            earthquakes[max_id]['Location_Description'] = max_loc_description
            earthquakes[max_id]['Time'] = max_time
        elif mag ==max_mag:
            # Append to dict
            max_id = get_earthquake_id(earthquake)
            max_mag = mag
            max_loc = get_location(earthquake)
            max_loc_description =get_location_description(earthquake)
            max_time = get_time(earthquake)
            earthquakes[max_id] ={}
            earthquakes[max_id]['Magnitude'] = max_mag
            earthquakes[max_id]['Location'] = max_loc
            earthquakes[max_id]['Location_Description'] = max_loc_description
            earthquakes[max_id]['Time'] = max_time

    #return max_mag, max_loc, max_loc_description, max_time
    return earthquakes



# Load the data
data = get_data()
print(f"Loaded {count_earthquakes(data)} \n")

# Analyse the data
max_earthquakes= get_maximum(data)

# Print summary of analysis
print(f'There are {len(max_earthquakes)} earthquakes with the strongest magnitude in the range.\n')
for earthquake in max_earthquakes:
    print(f"The strongest earthquake(s) were at {max_earthquakes[earthquake]['Location']}, {max_earthquakes[earthquake]['Location_Description']}, with magnitude {max_earthquakes[earthquake]['Magnitude']}, on {max_earthquakes[earthquake]['Time']}")
