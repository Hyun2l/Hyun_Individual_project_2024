import fastf1
from fastf1 import get_event_schedule, get_session
import pandas as pd

# Enable caching to speed up repeated requests

def get_full_season_data(year):
    # Get the list of events for the season
    schedule = get_event_schedule(year)
    race_events = schedule[schedule['EventFormat'] == 'conventional']

    # Containers for our data
    all_combined_data = []

    # Loop through each race event in the season
    for _, event in race_events.iterrows():
        race_name = event['EventName']
        try:
            # Load race session data
            session = get_session(year, race_name, 'R')
            session.load(laps=True, telemetry=True, weather=True)

            # Get lap and telemetry data
            laps = session.laps
            laps['RaceName'] = race_name  # Add race name for context

            # Get session results
            results = session.results
            results_df = pd.DataFrame(results)
            results_df['RaceName'] = race_name  # Add race name for context

            # Combine lap data with results
            combined_data = pd.merge(
                laps[['LapNumber', 'DriverNumber', 'LapTime', 'TrackStatus', 'RaceName']],
                results_df,
                on=['DriverNumber', 'RaceName'],
                how='left'
            )

            # Add telemetry data
            for _, lap in laps.iterlaps():
                telemetry = lap[1].get_telemetry()
                telemetry['LapNumber'] = lap[1]['LapNumber']
                combined_data = pd.merge(
                    combined_data,
                    telemetry,
                    on=['LapNumber', 'RaceName'],
                    how='left'
                )

            # Append combined data for this race to the season's list
            all_combined_data.append(combined_data)

        except Exception as e:
            print(f"Error processing {race_name}: {e}")

    # Concatenate all combined data into one DataFrame for the season
    full_season_data = pd.concat(all_combined_data, ignore_index=True)
    return full_season_data

def save_to_csv(data, filename):
    data.to_csv(filename, index=False)

# Main execution
season_data = get_full_season_data(2021)
save_to_csv(season_data, '2021_f1_season_full_data.csv')
