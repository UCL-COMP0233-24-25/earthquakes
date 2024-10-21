import os
from datetime import date
import numpy as np

import matplotlib.pyplot as plt
import json
import requests
from jedi.inference.finder import filter_name
from matplotlib.pyplot import pause


def get_data(force_download = False):
    """Retrieve the data we will be working with."""
    "if the file is exist, just use the file instead of download"
    file_name = 'earthquake_data.json'

    if os.path.exists(file_name) and not force_download:
        with open(file_name, 'r') as f:
            dic = json.load(f)
    else:
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
        text = response.text
        dic = json.loads(text)
        with open(file_name, 'w') as f:
            json.dump(dic, f)
    return dic


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
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.

    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """

    res = {}
    for earthquake in earthquakes:
        year = get_year(earthquake)
        if year in res:
            lst = res[year]
        else:
            lst = []
            res[year] = lst
        lst.append(get_magnitude(earthquake))
    return res


def plot_average_magnitude_per_year(earthquakes):
    plt.figure(figsize=(11, 4.8))
    dic = get_magnitudes_per_year(earthquakes)
    years = []
    avgs = []
    for year in dic:
        years.append(year)
        avgs.append(np.mean(dic[year]))

    plt.bar(years, avgs)
    plt.xlabel("years")
    plt.ylabel("magnitude per year")
    plt.xticks([i for i in range(np.min(years), np.max(years)+1)])
    plt.savefig("average_magnitude_per_year.png")


def plot_number_per_year(earthquakes):
    plt.figure(figsize=(11, 4.8))
    dic = get_magnitudes_per_year(earthquakes)
    years = []
    nums = []
    for year in dic:
        years.append(year)
        nums.append(len(dic[year]))

    plt.bar(years, nums)
    plt.xlabel("years")
    plt.ylabel("number per year")
    plt.xticks([i for i in range(np.min(years), np.max(years)+1)])
    plt.savefig("number_per_year.png")



# Get the data we will work with
quakes = get_data()['features']


# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)
