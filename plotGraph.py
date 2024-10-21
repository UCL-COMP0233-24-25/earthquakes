from datetime import date

import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np

def get_data():
    with open("xtfile.json","r") as f:
        data = json.load(f)
        
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
    """Retrive the magnitude of an earthquake item."""
    return earthquake['properties'].get('mag', None)


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    magnitudes_per_year = {}
    for earthquake in earthquakes:
        if(magnitudes_per_year.__contains__(get_year(earthquake))):
            magnitudes_per_year[get_year(earthquake)].append(get_magnitude(earthquake))
        else:
            magnitudes_per_year[get_year(earthquake)]=[get_magnitude(earthquake)]
    return magnitudes_per_year

def plot_average_magnitude_per_year(earthquakes):
    
    data = get_magnitudes_per_year(earthquakes)
    average_magnitude=[]
    for key in data:
        average_magnitude.append(sum(data[key])/len(data[key]))
    x = data.keys()
    y = average_magnitude
    plt.plot(x,y)
    plt.xticks(range(min(x),max(x)+1),rotation=-45)
    plt.title("average magnitude per year")
    plt.xlabel("year")
    plt.ylabel("magnitude")


def plot_number_per_year(earthquakes):
    data = get_magnitudes_per_year(earthquakes)
    average_number=[]
    for key in data:
        average_number.append(len(data[key]))
    x = data.keys()
    y = average_number
    plt.bar(x,y)
    plt.xticks(range(min(x),max(x)+1),rotation=-45)
    plt.title("number per year")
    plt.xlabel("year")
    plt.ylabel("number")


# Get the data we will work with
quakes = get_data()["features"]


# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plt.subplot(2, 1, 1)
plot_number_per_year(quakes)

plt.subplot(2, 1, 2)
plot_average_magnitude_per_year(quakes)

plt.subplots_adjust(hspace=1)