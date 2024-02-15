import fastf1
import pandas as pd
from fastf1.core import Laps

def get_race_data(year, race):
    # Get the session data
    session = fastf1.get_session(year, race, 'R')
    session.load()

    # Extracting laps data for all drivers
    laps = session.laps
    # Selecting relevant columns
    laps = laps[['DriverNumber', 'LapNumber', 'LapTime', 'TrackStatus', 'weather_data''IsAccurate']]





    # You can add more data from the laps if required
    # laps['Compound'] = laps['Compound']
    # laps['TyreLife'] = laps['TyreLife']
    # laps['Stint'] = laps['Stint']

    return laps

def save_to_csv(data, filename):
    data.to_csv(filename, index=False)

# Example usage
race_data = get_race_data(2019, 'Monaco')  # Replace with desired year and race
save_to_csv(race_data, '2019_monaco_race_data.csv')  # Saves the data to '2019_monaco_race_data.csv'

#%%
