import fastf1
import pandas as pd
from fastf1 import get_event_schedule


def get_race_data_for_season(year):
    all_races_data = pd.DataFrame()  # Data frame to store data from all races


    schedule = get_event_schedule(year)
    race_events = schedule[schedule['EventFormat'] == 'conventional']  ## Filter only the race events

    for _, event in race_events.iterrows():
        race_name = event['EventName']
        try:
            # Load session data
            session = fastf1.get_session(year, race_name, 'R') # R : Race
            session.load()

            # Extracting laps data for all drivers
            laps = session.laps
            laps = laps[['DriverNumber', 'LapNumber', 'LapTime', 'TrackStatus', 'IsAccurate']]
            laps['RaceName'] = race_name  # Add race name for identification

            # Append this race's data to the main DataFrame
            """ TrackStatus Description: 
            ‘1’: Track clear (beginning of session or to indicate the end of another status)
            ‘2’: Yellow flag (sectors are unknown)
            ‘3’: ??? Never seen so far, does not exist?
            ‘4’: Safety Car
            ‘5’: Red Flag
            ‘6’: Virtual Safety Car deployed
            ‘7’: Virtual Safety Car ending (As indicated on the drivers steering wheel, on tv and so on; status ‘1’ will mark the actual end) """

            all_races_data = all_races_data.append(laps, ignore_index=True)
        except Exception as e:
            print(f"Error processing {race_name}: {e}")

    return all_races_data

def save_to_csv(data, filename):
    data.to_csv(filename, index=False)

# Example usage
season_data = get_race_data_for_season(2019)
save_to_csv(season_data, '2019_f1_season_data.csv')
