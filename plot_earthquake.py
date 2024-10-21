from datetime import date
import json
import matplotlib.pyplot as plt



def get_data():
    """Retrieve the data we will be working with."""
    with open('jsonfile.json','r') as f:
        loaded_json_str=f.read()
    load=json.loads(loaded_json_str)

    return load


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
    ...


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes,year):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    mag=[]
    for i in range(len(earthquakes)):
        quake=earthquakes[i]
        mag.append(get_magnitude(quake))
    yearmag={year:mag}
    return yearmag

    ...


def plot_average_magnitude_per_year(yearquakes,year):
    avg=[]
    for i in range(len(year)):
        yearmag=get_magnitudes_per_year(yearquakes[i],year[i])
        mag=yearmag[year[i]]
        avg_mag=sum(mag)/len(mag)
        avg.append(avg_mag)
    plt.plot(year,avg)
    plt.xlabel("Years")
    plt.ylabel("avg_mag")
    plt.show()

    ...


def plot_number_per_year(earthquakes):
    year=[]
    for i in range(len(earthquakes)):
        quake=earthquakes[i]
        if get_year(quake) in year:
            continue
        else:
            year.append(get_year(quake))
    yearquakes=[]
    yearnum=[]
    for i in range(len(year)):
        temp=[]
        for j in range(len(earthquakes)):
            quake=earthquakes[j]
            if get_year(quake) == year[i]:
                temp.append(quake)
        yearquakes.append(temp)
        yearnum.append(len(temp))
    plt.plot(year,yearnum)
    plt.xlabel("Years")
    plt.ylabel("number of earthquakes")
    plt.show()
    return yearquakes,year
    ...



# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
yearquakes,year=plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(yearquakes,year)