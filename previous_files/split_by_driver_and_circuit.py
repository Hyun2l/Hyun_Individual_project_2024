from fastf1 import get_session
from fastf1 import get_event_schedule
import pandas as pd

def save_lap_and_telemetry_data_for_season(year, driver_code):
    all_laps_with_weather_telemetry_and_circuit = []

    schedule = get_event_schedule(year)
    race_events = schedule[schedule['EventFormat'] == 'conventional']

    for _, event in race_events.iterrows():
        race_name = event['EventName']
        session = get_session(year, race_name, 'R')  # Race only
        session.load(telemetry=True, laps=True, messages=True)

        # Get circuit information
        circuit_info = session.get_circuit_info()

        # Filter laps for the specific driver
        driver_laps = session.laps.pick_driver(driver_code)

        for lap in driver_laps.iterlaps():
            lap_data = lap[1].to_dict()
            weather_data = lap[1].get_weather_data().to_dict()

            lap_data['Circuit_Name'] = race_name  # Adding circuit name
            lap_data['Circuit_Corners'] = len(circuit_info.corners)  # Adding number of corners
            lap_data['Circuit_Rotation'] = circuit_info.rotation  # Adding circuit rotation
            lap_data.update(weather_data)

            all_laps_with_weather_telemetry_and_circuit.append(lap_data)

    # Convert to DataFrame and save as CSV
    combined_data = pd.DataFrame(all_laps_with_weather_telemetry_and_circuit)
    combined_data.to_csv(f'f1_{year}_{driver_code}_combined_data.csv', index=False)

# Example usage
save_lap_and_telemetry_data_for_season(2019, 'GAS')  # Replace 'HAM' with the actual driver code
