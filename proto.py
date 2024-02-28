import fastf1
from fastf1 import get_event_schedule
import pandas as pd

def save_lap_weather_data_for_season(year):
    all_laps_with_weather = []  # 모든 랩과 날씨 데이터를 저장할 리스트

    schedule = get_event_schedule(year)
    race_events = schedule[schedule['EventFormat'] == 'conventional']

    for _, event in race_events.iterrows():
        race_name = event['EventName']
        try:
            session = fastf1.get_session(year, race_name, 'R')
            session.load(telemetry=True,laps=True,messages=True)  # 텔레메트리 데이터 없이 세션 데이터 로드

            for lap in session.laps.iterlaps():
                lap_data = lap[1].to_dict()  # 랩 데이터를 딕셔너리로 변환
                weather_data = lap[1].get_weather_data().to_dict()  # 해당 랩의 날씨 데이터 조회
                lap_data.update(weather_data)  # 랩 데이터에 날씨 데이터 추가

                all_laps_with_weather.append(lap_data)  # 결과를 리스트에 추가





        except Exception as e:
            print(f"Error processing data for {race_name}: {e}")

    if all_laps_with_weather:
        # 모든 랩과 날씨 데이터를 포함하는 DataFrame 생성
        combined_data = pd.DataFrame(all_laps_with_weather)
        # CSV 파일로 저장
        combined_data.to_csv(f'f1_{year}_laps_with_weather_data.csv', index=False)
    else:
        print("No lap weather data to save.")

# 2019년 데이터 저장
save_lap_weather_data_for_season(2019)
