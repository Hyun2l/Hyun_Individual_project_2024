import datetime
import warnings

import fastf1
import pandas as pd
from fastf1.plotting import setup_mpl
from matplotlib import pyplot as plt

setup_mpl()


years = range(2022, 2023)  # Example: from 2018 to current year

all_stints_data = pd.DataFrame()

for year in years:
    print(f"Processing year: {year}")
    calendar = fastf1.get_event_schedule(year)
    for _, event in calendar.iterrows():
        gp = event['EventName']
        print(f"Processing event: {gp}")

        # Fetch session data
        session = fastf1.get_session(year, gp, 'R')
        session.load()
        laps = session.laps

        # Process data as in previous example
        drivers = session.drivers
        drivers = [session.get_driver(driver)["Abbreviation"] for driver in drivers]
        stints = laps[["Driver", "Stint", "Compound", "LapNumber"]]
        stints = stints.groupby(["Driver", "Stint", "Compound"]).count().reset_index()
        stints = stints.rename(columns={"LapNumber": "StintLength"})
        stints['Year'] = year
        stints['Event'] = gp

        # Append to the main DataFrame
        all_stints_data = all_stints_data.append(stints, ignore_index=True)

# Save the DataFrame to a file
all_stints_data.to_csv('/Users/hyun/Desktop/Individual Project/data/tire_strategy_data.csv', index=False)


#%%

#%%
