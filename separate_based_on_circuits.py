from fastf1 import get_session, get_event_schedule
import pandas as pd

def save_lap_and_telemetry_data_for_season_and_driver(year):
    schedule = get_event_schedule(year)
    race_events = schedule[schedule['EventFormat'] == 'conventional']

    for _, event in race_events.iterrows():
        race_name = event['EventName']
        try:
            session = get_session(year, race_name, 'R')  # Race only
            session.load(telemetry=True, laps=True, messages=True)

            # Get the list of drivers from the session results
            drivers = session.results['DriverNumber'].unique()

            for driver_code in drivers:
                # Filter laps for the specific driver
                driver_laps = session.laps.pick_driver(driver_code)

                all_laps_data = []

                for lap in driver_laps.iterlaps():
                    # Get the lap data as a dictionary
                    lap_data = lap[1].to_dict()
                    # Get the corresponding weather data for the lap
                    weather_data = lap[1].get_weather_data().to_dict()
                    # Update the lap data dictionary with weather data
                    lap_data.update(weather_data)
                    # Append this updated lap data to the all_laps_data list
                    all_laps_data.append(lap_data)

                # Create a DataFrame from the list of lap data dictionaries
                circuit_laps_df = pd.DataFrame(all_laps_data)
                # Save the DataFrame to a CSV file named after the race event and driver

                circuit_laps_df.to_csv(f"{driver_code}_{year}_{race_name}_data.csv", index=False)

        except Exception as e:
            print(f"Error processing {race_name}: {e}")

save_lap_and_telemetry_data_for_season_and_driver(2019)
