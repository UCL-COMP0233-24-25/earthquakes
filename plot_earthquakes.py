from datetime import date
import json
import requests
import matplotlib.pyplot as plt


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

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.json()
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    with open("response.json", "w") as f:
        json.dump(text, f, indent=4)
        
    return text


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

    mag_per_year = dict()
    for earthquake in earthquakes:
        year = get_year(earthquake)
        if year in mag_per_year:
            mag_per_year[year].append(get_magnitude(earthquake))
        else:
            mag_per_year[year] = [get_magnitude(earthquake)]
            
    return mag_per_year
    

def plot_average_magnitude_per_year(earthquakes):
    magnitude_dict = get_magnitudes_per_year(earthquakes)
    average_magnitude_map = {year: (sum(earthquake_mag)/len(earthquake_mag)) for year, earthquake_mag in magnitude_dict.items()}
    
    dates = list(average_magnitude_map.keys())
    magnitudes = list(average_magnitude_map.values())
    
    plt.figure(figsize=(8,5))
    plt.rcParams.update({'font.size': 8})
    fig = plt.gcf()
    ax = fig.add_subplot(111)

    ax.plot(dates,magnitudes,label="Slow method", color='red',ls='-',marker='X')

    ax.set_title('Average annual earthquake magnitude')
    ax.set_xticks(dates)
    ax.set_ylabel('Magnitude (richter scale)')
    ax.set_xlabel('Year')
    plt.show()


def plot_number_per_year(earthquakes):
    magnitude_dict = get_magnitudes_per_year(earthquakes)
    average_magnitude_map = {year: len(earthquake_mag) for year, earthquake_mag in magnitude_dict.items()}
    
    dates = list(average_magnitude_map.keys())
    numbers = list(average_magnitude_map.values())
    
    plt.figure(figsize=(8,5))
    plt.rcParams.update({'font.size': 8})
    fig = plt.gcf()
    ax = fig.add_subplot(111)

    ax.bar(dates,numbers,label="Slow method", color='red')

    ax.set_title('Annual Earthquake Frequency')
    ax.set_xticks(dates)
    ax.set_ylabel('Earthquake Frequency (Events per year)')
    ax.set_xlabel('Year')
    plt.show()


# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)