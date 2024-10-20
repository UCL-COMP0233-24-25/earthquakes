import requests
import json


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

    data = json.loads(response.text)

    return data

def count_earthquakes(data):
    return len(data['features'])


def get_magnitude(data, earthquake):
    return data['features'][earthquake]['properties']['mag']


def get_location(data, earthquake):
    latitude, longitude = data['features'][earthquake]['geometry']['coordinates'][:2]
    return latitude, longitude


def get_maximum(data):
    max_magnitude = 0
    max_location = None
    for earthquake in range(count_earthquakes(data)):
        magnitude = get_magnitude(data, earthquake)
        if magnitude > max_magnitude:
            max_magnitude = magnitude
            max_location = get_location(data, earthquake)
    return max_magnitude, max_location

data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")