# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json
import matplotlib.pyplot as plt
import datetime
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
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:

    data = response.json()

    with open("response.json", "w") as f:
        json.dump(data, f, indent=4)
    
    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return data

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""


    return len(data['features'])


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake['properties']['mag']


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    return earthquake['geometry']['coordinates'][:2]


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    max_magnitude = 0
    max_locations = []
    for earthquake in data['features']:
        magnitude = get_magnitude(earthquake)
        if magnitude > max_magnitude:
            max_magnitude = magnitude
            max_locations = [get_location(earthquake)]
        elif magnitude == max_magnitude:
            max_locations.append(get_location(earthquake))
    return max_magnitude, max_locations

def freq_per_yr_plot(plot=False):

    years_sec = [earthquake['properties']['time'] for earthquake in data['features']] 
    years = [datetime.datetime.fromtimestamp(year/1000).year for year in years_sec]

    year_counts = {}
    for year in years:
        if year in year_counts:
            year_counts[year] += 1
        else:
            year_counts[year] = 1
    if plot:
        plt.bar(year_counts.keys(), year_counts.values())
        plt.xticks(np.arange(2000, 2019, 1))
        plt.xlabel("Year")
        plt.ylabel("Number of Earthquakes")
        plt.title("Number of Earthquakes per Year")
        plt.show()
    return year_counts

def avg_mag_per_year(data, plot=False):
    cum_mag_per_year = {}
    quakes = [quake for quake in data['features']]
    for quake in quakes:
        quake_year = datetime.datetime.fromtimestamp(quake['properties']['time']/1000).year 
        quake_mag = quake['properties']['mag']
        if quake_year not in cum_mag_per_year.keys():
            cum_mag_per_year[quake_year] = quake_mag
        else:
            cum_mag_per_year[quake_year] += quake_mag
    year_counts = freq_per_yr_plot()
    for year in cum_mag_per_year:
        cum_mag_per_year[year] = cum_mag_per_year[year]/year_counts[year]
    if plot:
        plt.bar(year_counts.keys(), year_counts.values())
        plt.xticks(np.arange(2000, 2019, 1))
        plt.xlabel("Year")
        plt.ylabel("Average Magnitude")
        plt.title("Average Magnitude of Earthquakes per Year")
        plt.show()
    return cum_mag_per_year


# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")

  
avg_mag_per_year(data, plot=True)