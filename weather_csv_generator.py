import fastf1
from fastf1 import get_event_schedule
import pandas as pd
def save_weather_data_for_season(year):
    all_weather_data = []  #  a List to hold weather data DataFrames

    schedule = get_event_schedule(year)
    race_events = schedule[schedule['EventFormat'] == 'conventional']

    for _, event in race_events.iterrows():
        race_name = event['EventName']
        try:
            # Load the race session
            session = fastf1.get_session(year, race_name, 'R') # R == Race only
            session.load()


            # Get weather data for the session
            weather_data = session.weather_data
            weather_data['RaceName'] = race_name  # Add race name for reference
            weather_data['SessionTime'] = session.session_start_time
            weather_data['T0Date'] = session.t0_date


            all_weather_data.append(weather_data)

        except Exception as e:
            print(f"Error processing weather data for {race_name}: {e}") # Error handling provided from the API

    # Combine all weather data into a single DataFrame
    combined_weather_data = pd.concat(all_weather_data, ignore_index=True)

    # Save to CSV
    combined_weather_data.to_csv(f'f1_{year}_weather_data.csv', index=False)

# Swap the years
save_weather_data_for_season(2019)
