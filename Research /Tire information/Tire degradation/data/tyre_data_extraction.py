import fastf1 as ff1
from fastf1.core import Laps

# Enable caching for faster data loading
ff1.Cache.enable_cache('/Users/hyun/Desktop/Individual_Project/data/prototype_database')  # specify your cache directory

# Load session data (e.g., 2022 Bahrain GP, Race)
session = ff1.get_session(2021, 'Hungary ', 'R')  # Replace with your desired session
session.load()

laps = session.laps
tire_data = laps[['DriverNumber', 'LapNumber', 'Compound', 'TyreLife', 'FreshTyre']]


tire_data.to_csv('tire_data.csv', index=False)
