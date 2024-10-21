# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
from datetime import date
import matplotlib.pyplot as plt
import json
import random
import numpy as np

def get_data():
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
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data: {response.status_code}")
    return None


def explore_structure(data, indent=0):
    """
    Recursively explores and prints the structure of the JSON data.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            print("  " * indent + f"{key}: {type(value)}")
            explore_structure(value, indent + 1)
    elif isinstance(data, list):
        print("  " * indent + f"List of {len(data)} elements")
        if len(data) > 0:
            print("  " * indent + f"First element type: {type(data[0])}")
            explore_structure(data[0], indent + 1)
    else:
        print("  " * indent + f"{type(data)}")


# Check how deep a nested dictionary or list is
def find_max_depth(data, current_depth=0):
    """
    Determines the maximum depth of the nested JSON structure.
    """
    if isinstance(data, dict):
        return max(find_max_depth(value, current_depth + 1) for value in data.values())
    elif isinstance(data, list):
        return max(find_max_depth(item, current_depth + 1) for item in data)
    else:
        return current_depth

# Function to save the group to a JSON file
def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")

# Function to load the group from a JSON file
def load_from_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def count_earthquakes(data):
    """Get the total number of earthquakes in the dataset."""
    return len(data["features"]) if "features" in data else 0


def get_magnitude(earthquake):
    """Retrives the magnitude of an earthquake."""
    return earthquake["properties"].get("mag", None)


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    place = earthquake["properties"].get("place", "Unknown location")
    coordinates = earthquake["geometry"].get("coordinates", [None, None, None])
    longitude, latitude, depth = coordinates[0], coordinates[1], coordinates[2] if len(coordinates) == 3 else (None, None, None)
    
    return place, latitude, longitude, depth
    


def get_maximum(data):
    """
    Finds and returns the strongest earthquake in the dataset based on magnitude.
    """
    max_quake = None
    max_magnitude = float('-inf')

    for earthquake in data["features"]:
        mag = get_magnitude(earthquake)
        if mag is not None and mag > max_magnitude:
            max_magnitude = mag
            max_quake = earthquake
    
    return max_quake, max_magnitude

def get_year(data):
    """Extract the year in which an earthquake happened."""
    for earthquake in data["features"]:
        timestamp = earthquake["properties"]["time"]
        # The time is given in a strange-looking but commonly-used format.
        # To understand it, we can look at the documentation of the source data:
        # https://earthquake.usgs.gov/data/comcat/index.php#time
        # Fortunately, Python provides a way of interpreting this timestamp:
        # (Question for discussion: Why do we divide by 1000?)
        year = date.fromtimestamp(timestamp/1000).year
        earthquake["properties"]["year"] = year
    
    return {feature["properties"].get("year") for feature in data["features"]}

        

def get_magnitudes_per_year(data):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    new_data = {}
    unique_years = {feature["properties"].get("year") for feature in data["features"]}
    for year in unique_years:
        earthquakes_year = [feature for feature in data["features"] if feature["properties"].get("year") == year]
        frequency = len(earthquakes_year)
        mean_magnitude = np.mean([get_magnitude(earthquake) for earthquake in earthquakes_year])
        new_data[year] = {"frequency": frequency, "mean_magnitude": mean_magnitude}
    
    return new_data, unique_years

  

            





def plot_average_magnitude_per_year(earthquakes):
    ...


def plot_number_per_year(earthquakes):
    ...










if __name__ == "__main__":        
    # Step 1: Retrieve the earthquake data
    earthquake_data = get_data()
    #earthquake_data = earthquake_data["features"]
    get_year(earthquake_data)
    plot_data, years = get_magnitudes_per_year(earthquake_data)
    
    if earthquake_data:
        # Step 2: Explore the structure of the data
        # print("Data structure:")
        # explore_structure(earthquake_data)
        # print("\nMaximum depth of the JSON structure:", find_max_depth(earthquake_data))

        # Step 3: Count the number of earthquakes
        total_earthquakes = count_earthquakes(earthquake_data)
        print("\nTotal number of earthquakes:", total_earthquakes)
        # Step 4: Save the data as a json file
        ####save_to_json('earthquakes_data.json', earthquake_data)

        # Step 5: Find the strongest earthquake
        strongest_earthquake, max_magnitude = get_maximum(earthquake_data)
        if strongest_earthquake:
            place, lat, lon, depth = get_location(strongest_earthquake)
            print(f"\nStrongest earthquake:")
            print(f"  Location: {place}")
            print(f"  Magnitude: {max_magnitude}")
            print(f"  Coordinates: Latitude {lat}, Longitude {lon}, Depth {depth}")
        else:
            print("No earthquakes found.")
    




    

