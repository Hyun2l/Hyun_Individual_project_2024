import fastf1
import pandas as pd


def get_specific_year_data(year):
    specific_year_data = pd.DataFrame()

    schedule = fastf1.get_event_schedule(year)
    race_events = schedule[schedule['EventFormat'] == 'conventional']


    for _, event in race_events.iterrows():
        race_name = event['RaceName']













season_data = get_specific_year_data(2019)