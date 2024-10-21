import requests
# 10pm

import json
from datetime import date
import matplotlib.pyplot as plt


def get_data():
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            "starttime": "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc",
        },
    )

    text = response.text
    jsonText = json.loads(text)

    return jsonText


def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake["properties"]["time"]
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    year = date.fromtimestamp(timestamp / 1000).year
    return year


def get_magnitude(earthquake):
    return earthquake["properties"]["mag"]


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    output = {}
    for earthquake in earthquakes:
        Year = get_year(earthquake)
        Mag = get_magnitude(earthquake)
        output.setdefault(Year, []).append(Mag)
    return output


def plot_average_magnitude_per_year(earthquakes):
    output = get_magnitudes_per_year(earthquakes)
    Avg = {
        year: sum(magnitudes) / len(magnitudes) for year, magnitudes in output.items()
    }

    date = list(Avg.keys())
    value = list(Avg.values())
    plt.plot(date, value)
    plt.show


def plot_number_per_year(earthquakes):
    output = get_magnitudes_per_year(earthquakes)
    Avg = {year: sum(magnitudes) for year, magnitudes in output.items()}

    date = list(Avg.keys())
    value = list(Avg.values())
    plt.plot(date, value)
    plt.show


# Get the data we will work with
quakes = get_data()["features"]

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)
