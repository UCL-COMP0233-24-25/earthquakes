from datetime import date
import matplotlib.pyplot as plt
import json
# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests


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
    text = response.text
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    with open("earthquakes_data.json", 'w') as f:
        json.dump(response.json(), f, indent=4)
    return json.loads(text)


def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return data["metadata"]["count"]


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    coordinates = earthquake["geometry"]["coordinates"]
    # There are three coordinates, but we don't care about the third (altitude)
    return (coordinates[0], coordinates[1])


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    current_max_magnitude = get_magnitude(data["features"][0])
    current_max_location = get_location(data["features"][0])
    for item in data["features"]:
        magnitude = get_magnitude(item)
        # Note: what happens if there are two earthquakes with the same magnitude?
        if magnitude > current_max_magnitude:
            current_max_magnitude = magnitude
            current_max_location = get_location(item)
    return current_max_magnitude, current_max_location
    # There are other ways of doing this too:
    # biggest_earthquake = sorted(data["features"], key=get_magnitude)[0]
    # return get_magnitude(biggest_earthquake), get_location(biggest_earthquake)
    # Or...
    # biggest_earthquake = max(
    #     ({"mag": get_magnitude(item), "location": get_location(item)}
    #     for item in data["features"]),
    #     key=lambda x: x["mag"]
    # )
    # return biggest_earthquake["mag"], biggest_earthquake["location"]


def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    year = date.fromtimestamp(timestamp / 1000).year
    return year


def plot_number_per_year(earthquakes):
    frequency = [0] * 19
    for earthquake in earthquakes["features"]:
        year = get_year(earthquake)
        frequency[year - 2000] += 1

    years = list(range(2000, 2019, 1))

    plt.plot(years, frequency, marker='o')
    plt.xticks(ticks=[int(y) for y in years], rotation=60)
    plt.title("Earthquakes Frequency")
    plt.xlabel("year")
    plt.ylabel("earthquake in particular year")
    plt.show()


def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.

    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    mag_per_year = [0] * 19
    for earthquake in earthquakes["features"]:
        year = get_year(earthquake)
        mag_per_year[year - 2000] += get_magnitude(earthquake)

    return mag_per_year


def plot_average_magnitude_per_year(earthquakes):
    mag_per_year = get_magnitudes_per_year(earthquakes)
    frequency = [0] * 19
    for earthquake in earthquakes["features"]:
        year = get_year(earthquake)
        frequency[year - 2000] += 1

    average_mag_per_year = []
    for i in range(len(mag_per_year)):
        if frequency[i] != 0:
            average_mag_per_year.append(mag_per_year[i] / frequency[i])
        else:
            average_mag_per_year.append(0)

    years = list(range(2000, 2019, 1))

    plt.plot(years, average_mag_per_year, marker='o')
    plt.xticks(ticks=[int(y) for y in years], rotation=60)
    plt.title("Earthquakes magnitude")
    plt.xlabel("year")
    plt.ylabel("average earthquake magnitude in particular year")
    plt.show()


def main():
    # With all the above functions defined, we can now call them and get the result
    data = get_data()
    plot_number_per_year(data)
    plot_average_magnitude_per_year(data)


if __name__ == '__main__':
    main()
