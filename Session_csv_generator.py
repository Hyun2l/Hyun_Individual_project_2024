import fastf1
from fastf1 import get_event_schedule
import pandas as pd

def get_race_data_for_season(year):
    all_races_data = []  #  a list to collect data frames

    schedule = get_event_schedule(year)
    race_events = schedule[schedule['EventFormat'] == 'conventional']

    for _, event in race_events.iterrows():
        race_name = event['EventName']
        try:
            session = fastf1.get_session(year, race_name, 'R') # R: Race
            session.load(laps=True, weather=True)

            laps = session.laps
            laps_df = laps[['DriverNumber', 'LapNumber', 'LapTime', 'TrackStatus', 'Driver', 'Compound', 'TyreLife', 'IsAccurate','']]
            laps_df['RaceName'] = race_name  # Corrected to modify laps_df

            #session info to laps_df
            laps_df['SessionStart'] = session.session_start_time
            laps_df['T0Date'] = session.t0_date


            all_races_data.append(laps_df)  # Append current race's laps_df to the list

        except Exception as e:
            print(f"Error processing {race_name}: {e}")

    #all data frames into a single DataFrame
    combined_season_data = pd.concat(all_races_data, ignore_index=True)

    return combined_season_data

def save_to_csv(data, filename):
    data.to_csv(filename, index=False)

# Example usage
season_data = get_race_data_for_season(2021)
save_to_csv(season_data, '2021_f1_season_data.csv')
