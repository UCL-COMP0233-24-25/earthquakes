from datetime import date
import numpy as np
import json 
import os
import matplotlib.pyplot as plt


def get_data():
    #See earthquakes.py to access data from online database
    #Extra info specifying file path - ONLY FOR MY PERSONAL COMPUTER (I work in a VS code workspace, where the directory initialized is not the 
    # same as the directory where this file is hence I add \Week 4\earthwuakes\earthquakes_data.json)
    file_loc = os.path.join(os.getcwd(),'Week 4','earthquakes','earthquakes_data.json')
    
    #Access json file and load the json database as a Python dictionary
    with open(file_loc) as json_data_in:
        data = json.load(json_data_in)
    return data
    

def get_year(data):
    raw_t, t = [], []
    for event in data['features']:
        raw_t = event['properties']['time']
        t.append(date.fromtimestamp(raw_t/1000).year)
    return np.array(t)


def get_magnitude(data):
    mag = []
    for event in data['features']:
        m = event['properties']['mag']
        mag.append(m)
    return np.array(mag)


#Determine only the frequency of earthquakes
def get_magnitudes_per_year(Event_year, Event_mag, Avg_flag=False, Fre_flag=False):
    Total_years = np.arange(start=np.min(Event_year),stop=(np.max(Event_year)+1))

    
    Event_frequency = np.zeros(len(Total_years))
    Avg_mag = np.zeros(len(Total_years))
    
    for k in range(len(Total_years)):
        for j in range(len(Event_year)):
            if Total_years[k] == Event_year[j]:
                Event_frequency[k] += 1
        
        
        Mag_year = 0 
        if Event_frequency[k] != 0:
            for j in range(len(Event_year)):
                if Total_years[k] == Event_year[j]:
                    Mag_year += Event_mag[j]
        
            Avg_mag[k] = Mag_year/Event_frequency[k]
            
        else:
            continue     
    if Avg_flag:
        return Total_years, Avg_mag, Total_years
    elif Fre_flag:
        return Total_years, Event_frequency, Total_years


def plot_average_magnitude_per_year(data):
    Event_year = get_year(data)
    Event_mag = get_magnitude(data)
    
    Total_years, Avg_mag, Total_years = get_magnitudes_per_year(Event_year=Event_year,Event_mag=Event_mag,Avg_flag=True)
    
    plt.figure(figsize=(24,16))
    plt.rcParams.update({'font.size': 20})
    fig = plt.gcf()
    ax = fig.add_subplot(111)

    ax.plot(Total_years,Avg_mag,label="Slow method", color='red',ls='-',marker='X')

    ax.set_title('Average annual earthquake magnitude')
    ax.set_xticks(Total_years)
    #ax.set_ylim(0)
    #ax.set_xlim(2000)
    ax.set_ylabel('Magnitude (richter scale)')
    ax.set_xlabel('Year')
    plt.grid()


    plt.savefig(os.path.join(os.getcwd(),'Week 4','earthquakes','Avg_mag_per_year.png'))


def plot_number_per_year(data):
    Event_year = get_year(data)
    Event_mag = get_magnitude(data)
    
    Total_years, Event_frequency, Total_years = get_magnitudes_per_year(Event_year=Event_year,Event_mag=Event_mag,Fre_flag=True)
    
    plt.figure(figsize=(24,16))
    plt.rcParams.update({'font.size': 20})
    fig = plt.gcf()
    ax = fig.add_subplot(111)

    ax.bar(Total_years,Event_frequency,label="Slow method", color='red')

    ax.set_title('Annual Earthquake Frequency')
    ax.set_xticks(Total_years)
    ax.set_ylabel('Earthquake Frequency (Events per year)')
    ax.set_xlabel('Year')
    plt.grid()


    plt.savefig(os.path.join(os.getcwd(),'Week 4','earthquakes','Freq_per_year.png'))



# Get the data we will work with
data = get_data()

plot_number_per_year(data)

plt.clf()  # This clears the figure, so that we don't overlay the two plots

plot_average_magnitude_per_year(data)