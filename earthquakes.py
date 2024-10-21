import requests
import json
from datetime import date
import os
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

    data = json.loads(response.text)

    return data


def count_earthquakes(data):
    return len(data["features"])


def get_magnitude(data, earthquake):
    return data["features"][earthquake]["properties"]["mag"]


def get_location(data, earthquake):
    latitude, longitude = data["features"][earthquake]["geometry"]["coordinates"][:2]
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


def get_year(earthquake):
    timestamp = earthquake["properties"]["time"]
    year = date.fromtimestamp(timestamp / 1000).year
    return year


def get_magnitudes_per_year(data):
    """Retrieve the magnitudes of all the earthquakes in a given year.

    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    magnitudes_per_year = {}
    for earthquake in data["features"]:
        year = get_year(earthquake)
        magnitude = earthquake["properties"]["mag"]
        if year not in magnitudes_per_year:
            magnitudes_per_year[year] = []
        magnitudes_per_year[year].append(magnitude)
    return magnitudes_per_year


def plot_average_magnitude_per_year(data):
    magnitudes_per_year = get_magnitudes_per_year(data)
    average_magnitude_per_year = {
        year: sum(mags) / len(mags) for year, mags in magnitudes_per_year.items()
    }

    years = sorted(average_magnitude_per_year.keys())
    average_magnitudes = [average_magnitude_per_year[year] for year in years]

    plt.figure(figsize=(10, 5))
    plt.plot(years, average_magnitudes, marker="o")
    plt.title("Average Earthquake Magnitude per Year")
    plt.xlabel("Year")
    plt.ylabel("Average Magnitude")
    plt.xticks(range(min(years), max(years) + 1, 1))
    plt.grid(True)
    if not os.path.exists("plots"):
        os.makedirs("plots")
    plt.savefig(os.path.join("plots", "average_magnitude_per_year.png"))


def plot_number_per_year(data):
    magnitudes_per_year = get_magnitudes_per_year(data)
    number_per_year = {year: len(mags) for year, mags in magnitudes_per_year.items()}

    years = sorted(number_per_year.keys())
    number_of_earthquakes = [number_per_year[year] for year in years]

    plt.figure(figsize=(10, 5))
    plt.bar(years, number_of_earthquakes)
    plt.title("Number of Earthquakes per Year")
    plt.xlabel("Year")
    plt.xticks(range(min(years), max(years) + 1, 1))
    plt.ylabel("Number of Earthquakes")
    plt.yticks(range(0, max(number_of_earthquakes) + 1, 1))
    plt.grid(True)
    if not os.path.exists("plots"):
        os.makedirs("plots")
    plt.savefig(os.path.join("plots", "number_per_year.png"))


data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")

plot_number_per_year(data)
plot_average_magnitude_per_year(data)
