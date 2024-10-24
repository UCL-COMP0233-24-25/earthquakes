# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import date


def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
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
            "orderby": "time-asc"
            }
    )

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    
    with open("earthquake_data.json", "w") as file:
        json.dump(json.loads(text), file, indent=4)
    # See the README file for more information.
    data = json.loads(text)

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return data

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return data["metadata"]["count"]


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake['properties']['mag']


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    coordinates = earthquake['geometry']['coordinates']
    latitude = coordinates[1]
    longitude = coordinates[0]
    return latitude, longitude


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    max_magnitude = float('-inf')  # Initialize to a very low value to ensure any magnitude will be larger
    strongest_earthquake = None

    for earthquake in data['features']:
        local_magnitude = get_magnitude(earthquake)
        if local_magnitude > max_magnitude:
            max_magnitude = local_magnitude
            strongest_earthquake = earthquake

    # Extract the location of the strongest earthquake
    max_location = strongest_earthquake['properties']['place'] if strongest_earthquake else None
    return max_magnitude, max_location

def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # (Question for discussion: Why do we divide by 1000?)---convert milliseconds(unix) to seconds(python)
    year = date.fromtimestamp(timestamp/1000).year
    return year            
        
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """        
    mpy = {}
    for quake in earthquakes:
        year = get_year(quake)
        magnitude = get_magnitude(quake)
        if year not in mpy:
            mpy[year] = []
        mpy[year].append(magnitude)
        
    all_years = range(min(mpy), max(mpy) + 1)
    for year in all_years:
        if year not in mpy:
            mpy[year] = []
    ## The cases that some years didnt have earthquake
    return mpy

def plot_average_magnitude_per_year(earthquakes):
    """Plot the average magnitude of earthquakes per year."""
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    
    years = sorted(magnitudes_per_year.keys())
    avg_magnitudes = [
        sum(magnitudes_per_year[year]) / len(magnitudes_per_year[year]) if len(magnitudes_per_year[year]) > 0 else 0
        for year in years
    ]
    
    plt.figure()
    plt.plot(years, avg_magnitudes, marker='o', color='orange', linestyle='-', linewidth=2)
    plt.xlabel("Year")
    plt.ylabel("Average Magnitude")
    plt.title("Average Earthquake Magnitude per Year")
    plt.xticks(years, rotation=45)
    # plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_number_per_year(earthquakes):
    """Plot the number of earthquakes per year."""
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    
    years = sorted(magnitudes_per_year.keys())
    counts = [len(magnitudes_per_year[year]) for year in years]
    
    plt.figure()
    plt.bar(years, counts, color='skyblue')
    plt.xlabel("Year")
    plt.ylabel("Number of Earthquakes")
    plt.title("Number of Earthquakes per Year")
    plt.xticks(years, rotation=45)
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
        

# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")


quakes = get_data()['features']
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)
