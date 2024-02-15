import fastf1
import pandas as pd
from fastf1 import plotting
from fastf1.core import Laps


def get_race_data(year, race):
    # Get the session data
    session = fastf1.get_session(year, race, 'R')
    session.load()

    # Extracting laps data
    laps = session.laps
    laps = laps[['DriverNumber', 'LapNumber', 'LapTime', 'Compound', 'TyreLife', 'Stint', 'TrackStatus', 'IsAccurate']]

    # Extracting telemetry data
    telemetry = laps.pick_driver('44').get_car_data().add_distance()  # Example for one driver (number '44')

    # Merge laps data with telemetry data
    lap_telemetry = pd.merge(laps, telemetry, how='left', on=['DriverNumber', 'LapNumber'])

    return lap_telemetry

def save_to_csv(data, filename):
    data.to_csv(filename, index=False)

# Example usage
race_data = get_race_data(2022, 'Monaco Grand Prix')  # Replace with desired year and race
save_to_csv(race_data, 'race_data.csv')  # Saves the data to 'race_data.csv'



#%%
