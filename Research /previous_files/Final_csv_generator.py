from fastf1 import get_session, get_event_schedule
import fastf1
import pandas as pd

def save_all_laps_and_telemetry_data_for_driver_and_years(start_year, end_year, driver_code):
    all_years_data = []  # Initialize a list to hold data from all years

    for year in range(start_year, end_year + 1):
        schedule = get_event_schedule(year)

        race_events = schedule[schedule['EventFormat'] == 'conventional']

        for _, event in race_events.iterrows():
            race_name = event['EventName']
            try:
                session = get_session(year, race_name, 'R')  # Race only
                session.load(telemetry=False, laps=True, messages=True)

                # Filter laps for the specific driver
                driver_laps = session.laps.pick_driver(driver_code)

                for lap in driver_laps.iterlaps():
                    # Get the lap data as a dictionary
                    lap_data = lap[1].to_dict()
                    # Get the corresponding weather data for the lap
                    weather_data = lap[1].get_weather_data().to_dict()
                    # Update the lap data dictionary with weather data
                    lap_data.update(weather_data)
                    # Add circuit name and year to the lap data
                    lap_data['Circuit'] = race_name
                    lap_data['Year'] = year
                    # Append this updated lap data to the all_years_data list
                    all_years_data.append(lap_data)

            except Exception as e:
                print(f"Error processing {race_name} in {year}: {e}")

    # Create a DataFrame from the list of lap data dictionaries for all selected years
    all_years_laps_df = pd.DataFrame(all_years_data)

    # Save the DataFrame to a CSV file named after the driver, including all selected years
    all_years_laps_df.to_csv(f"f1_{start_year}_to_{end_year}_{driver_code}_all_data.csv", index=False)

# Example usage: Save all lap and telemetry data for Lewis Hamilton from 2014 to 2022 into one file
save_all_laps_and_telemetry_data_for_driver_and_years(2014, 2022, 'HAM')
