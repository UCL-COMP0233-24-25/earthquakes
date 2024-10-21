from datetime import date

import matplotlib.pyplot as plt
import json
import requests
import numpy as np

def get_data():
    """Retrieve the data we will be working with."""
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
    earthquake_text = response.text
    data = json.loads(earthquake_text)
    
    return data


def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    year = date.fromtimestamp(timestamp/1000).year
    return year


def get_magnitude(earthquake):
    x = earthquake["properties"]["mag"]
    return x


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    magnitudes_per_year = {}

    for earthquake in earthquakes:
        if (year:=get_year(earthquake)) in magnitudes_per_year:
            magnitudes_per_year[year].append(get_magnitude(earthquake))
        else:
            magnitudes_per_year[get_year(earthquake)] = [get_magnitude(earthquake)]
    return magnitudes_per_year
            


def plot_average_magnitude_per_year(earthquakes,ax):
    data=get_magnitudes_per_year(earthquakes)
    years = data.keys()
    average_magnitude = [np.mean(magnitudes) for magnitudes in data.values()]
    ax2=ax.twinx()
    ax2.plot(years,average_magnitude,color="red",label="Magnitude")
    ax2.set_ylabel("Average Magnitude")
    return



def plot_number_per_year(earthquakes,ax):
    data=get_magnitudes_per_year(earthquakes)
    years = data.keys()
    earthquake_count = [len(magnitudes) for magnitudes in data.values()]
    ax.bar(years,earthquake_count,label="Frequency")
    ax.set_xticks(range(1,len(years)))
    ax.set_xlabel("Year")
    ax.set_ylabel("Earthquake Frequency")
    return



# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
fig, ax = plt.subplots(nrows=1, ncols=1)
plot_number_per_year(quakes,ax)
plot_average_magnitude_per_year(quakes,ax)
plt.legend()
plt.show()