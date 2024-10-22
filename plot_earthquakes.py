from datetime import date

import matplotlib.pyplot as plt
import json

def get_data():
    """Retrieve the data we will be working with."""
    with open('earthquakes.json', 'r') as f:
        data = json.load(f) # json.load function which can be used to directly load a JSON formatted file in to a Python object
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
    return earthquake['properties']['mag']


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    year_dic = {}
    for earthquake in earthquakes:
        current_year = get_year(earthquake)
        current_mag = get_magnitude(earthquake)
        if current_year in year_dic:
            year_dic[current_year].append(current_mag)
        else:
            year_dic[current_year]=[current_mag]
    return year_dic

def plot_average_magnitude_per_year(earthquakes):
    year_dic = get_magnitudes_per_year(earthquakes)
    avg_mag_per_year = {key: sum(value)/len(value) for key,value in year_dic.items()}
    dates = list(avg_mag_per_year.keys())
    values = list(avg_mag_per_year.values())
    
    plt.figure(figsize=(12, 8))
    plt.plot(dates, values, '-o')
    
    plt.xlabel('Years')
    plt.xticks(dates, rotation=45) 
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))
    plt.ylabel('Frequency of earthquakes')
    
    plt.title('Frequency (number) of earthquakes per year')
    plt.savefig('./Frequency (number) of earthquakes per year.jpg')
    # plt.show()


def plot_number_per_year(earthquakes):
    earthquakes_dict = get_magnitudes_per_year(earthquakes)
    number_dict = {key: (sum(value)) for key, value in earthquakes_dict.items()}
    dates = list(number_dict.keys())
    values = list(number_dict.values())

    plt.figure(figsize=(12, 8))
    plt.plot(dates, values, '-o')
    
    plt.xlabel('Years')
    plt.xticks(dates, rotation=45) 
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))
    plt.ylabel('Average magnitude')
    
    plt.title('Average magnitude of earthquakes per year')
    plt.savefig('./Average magnitude of earthquakes per year.jpg')
    # plt.show()



# Get the data we will work with
quakes = get_data()['features']
# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)
