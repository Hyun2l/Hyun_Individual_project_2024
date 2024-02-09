import fastf1
import pandas as pd
from fastf1 import get_event_schedule

def get_race_data_for_season(year):
    all_races_data = pd.DataFrame()

    schedule = get_event_schedule(year)
    race_events = schedule[schedule['EventFormat'] == 'conventional']

    for _, event in race_events.iterrows():
        race_name = event['EventName']
        try:
            session = fastf1.get_session(year, race_name, 'R')
            session.load(laps = True, weather= True)

            weather_df = session.weather_data
            if weather_df['Time'].dtype == 'timedelta64[ns]':
                weather_df['Time'] = session.session_start_time + weather_df['Time']
            else:
                weather_df['Time'] = pd.to_datetime(weather_df['Time'])

            laps = session.laps
            laps = laps[['DriverNumber', 'LapNumber', 'LapTime', 'TrackStatus', 'IsAccurate']]
            laps['RaceName'] = race_name
            laps['Time'] = session.session_start_time + laps['Time']

            combined_data = pd.merge_asof(laps.sort_values('Time'), weather_df.sort_values('Time'), on='Time', by='RaceName')

            all_races_data = all_races_data.append(combined_data, ignore_index=True)
        except Exception as e:
            print(f"Error processing {race_name}: {e}")

    return all_races_data
def save_to_csv(data, filename):
    data.to_csv(filename, index=False)

# 사용 예
season_data = get_race_data_for_season(2021)
save_to_csv(season_data, '2021_f1_season_data_with_weather.csv')
