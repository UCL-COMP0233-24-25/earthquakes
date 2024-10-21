import requests
import json
import matplotlib.pyplot as plt


def get_data(start = '2000', end = '2018'):
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': f"{start}-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": f"{end}-12-31",
            "orderby": "time-asc"}
    )
    text = response.text
    data = json.loads(text)
    

    return data



def count_quakes(data):
    return len(data['features'])

def mag(earthquake):
    return(earthquake['properties']['mag'])

def average_mag(data):
    s = sum(float(eq['properties']['mag']) for eq in data['features'])
    q = count_quakes(data)
    if q == 0:
        return 0
        
    return s / q

quakes = []
years = []
mags = []
for year in range(2000, 2020):
    data = get_data(start = year, end = year)
    earthquakes = count_quakes(data)
    average = average_mag(data)
    
    quakes.append(earthquakes)
    mags.append(average)
    years.append(str(year))


plt.figure(figsize=(13, 6))
plt.bar(years, quakes)

plt.figure(figsize = (13,6))
plt.plot(years, mags)
plt.show()