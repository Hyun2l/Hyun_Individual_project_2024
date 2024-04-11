from fastf1 import get_session, get_event_schedule
import pandas as pd
import os

def save_lap_and_telemetry_data_for_season(year):
    schedule = get_event_schedule(year)
    race_events = schedule[schedule['EventFormat'] == 'conventional']


    for _, event in race_events.iterrows():

        race_name = event['EventName']
        session = get_session(year, race_name, 'R')  # Race only
        session.load(telemetry=True, laps=True, messages=True)

        # Create a directory for the circuit if it doesn't exist
        circuit_directory = f'{year}/{race_name}'
        if not os.path.exists(circuit_directory):
            os.makedirs(circuit_directory)

        # Get circuit information
        circuit_info = session.get_circuit_info()

        # Iterate over all drivers that participated in the session
        for driver in session.results['Abbreviation'].unique():
            driver_laps = session.laps.pick_driver(driver)
            all_laps_with_weather_telemetry_and_circuit = []



           # columns_to_drop = ['DeletedReason', 'FastF1Generated']
            for lap in driver_laps.iterlaps():
                lap_data = lap[1].to_dict()
                weather_data = lap[1].get_weather_data().to_dict()
                # Include any other desired information from session.results here

                finishing_position = session.results['Position']
                #grid_position = session.results['GridPosition']

                #lap_data['finishingPosition'] = finishing_position
                #lap_data['GridPosition'] = grid_position

                lap_data['Encoded_Rainfall'] = int(weather_data['Rainfall'])

                lap_data['Circuit_Name'] = race_name  # Adding circuit name
                lap_data['Circuit_Corners'] = len(circuit_info.corners)  # Adding number of corners
                lap_data['Circuit_Rotation'] = circuit_info.rotation  # Adding circuit rotation
                lap_data.update(weather_data)

                all_laps_with_weather_telemetry_and_circuit.append(lap_data)

            # Convert to DataFrame and save as CSV for each driver
            driver_data = pd.DataFrame(all_laps_with_weather_telemetry_and_circuit)

          #  driver_data = driver_data.drop(columns_to_drop,errors='ignore')

            # Reorder the columns to put 'LapTime' and 'Position' first
            cols = ['LapTime', 'Position','Driver','DriverNumber']  # Start with LapTime and Position
            cols.extend([col for col in driver_data.columns if col not in cols])  # Add the rest of the columns
            driver_data = driver_data[cols]



            driver_data.to_csv(f'{circuit_directory}/{driver}_laps.csv', index=False)


save_lap_and_telemetry_data_for_season(2020)
