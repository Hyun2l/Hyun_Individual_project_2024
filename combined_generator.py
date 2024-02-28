from fastf1 import get_session
import fastf1
from fastf1 import get_event_schedule
import pandas as pd

def save_lap_and_telemetry_data_for_season(year):
    all_laps_with_weather_telemetry_and_circuit = []

    schedule = get_event_schedule(year)
    race_events = schedule[schedule['EventFormat'] == 'conventional']

    for _, event in race_events.iterrows():
        race_name = event['EventName']
        session = get_session(year, race_name, 'R') # Race only
        session.load(telemetry=True,laps=True,messages=True)

        # Get circuit information
        circuit_info = session.get_circuit_info()

        for lap in session.laps.iterlaps():
            lap_data = lap[1].to_dict()
            weather_data = lap[1].get_weather_data().to_dict()
            #telemetry_data = lap[1].get_telemetry()


            lap_data['Circuit_Name'] = race_name  # Adding circuit name
            lap_data['Circuit_Corners'] = len(circuit_info.corners)  #  Adding number of corners
            lap_data['Circuit_Rotation'] = circuit_info.rotation  #  Adding circuit rotation
            #lap_data['Marshal_lights'] =circuit_info.marshal_lights
            #lap_data['Marshal_sectors'] = circuit_info.marshal_sectors
            #telemetry_data['Speed'] = telemetry_data['Speed']

            # Update lap data with weather and telemetry
            lap_data.update(weather_data)


            all_laps_with_weather_telemetry_and_circuit.append(lap_data)

    # Convert to DataFrame and save as CSV
    combined_data = pd.DataFrame(all_laps_with_weather_telemetry_and_circuit)
    combined_data.to_csv(f'f1_{year}_combined_data.csv', index=False)

save_lap_and_telemetry_data_for_season(2019)