import fastf1
from fastf1 import get_event_schedule
import pandas as pd

def save_race_data_for_season(year):
    all_races_data = []

    schedule = get_event_schedule(year)
    race_events = schedule[schedule['EventFormat'] == 'conventional']

    for _, event in race_events.iterrows():
        race_name = event['EventName']
        try:
            session = fastf1.get_session(year, race_name, 'R') # R: Race
            session.load(laps=True, weather=True)

            laps = session.laps
            laps_df = laps[['DriverNumber', 'LapNumber', 'LapTime', 'TrackStatus', 'Driver', 'Compound', 'TyreLife', 'IsAccurate']]
            laps_df['RaceName'] = race_name

            laps_df['SessionStart'] = session.session_start_time
            laps_df['T0Date'] = session.t0_date

            all_races_data.append(laps_df)
        except Exception as e:
            print(f"Error processing {race_name}: {e}")

    combined_season_data = pd.concat(all_races_data, ignore_index=True)

    # Save to CSV with a dynamically generated filename
    combined_season_data.to_csv(f'f1_{year}_session_data.csv', index=False)

# Example usage
save_race_data_for_season(2022)
