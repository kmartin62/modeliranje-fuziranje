import requests
from datetime import timedelta, date
import ast
import time
import csv
import json

csv_columns = ['timezone', 'country_code', 'station_id', 'relative_humidity', 'wind_speed',
               'sea_level_pressure', 'solar_elevation_angle', 'solar_radiation', 'pressure', 'snow',
               'uv', 'wind_direction', 'weather_description', 'visibility', 'clouds', 'date', 'time']

api_columns = [
    'timezone',
    'country_code',
    'station_id',
    'rh',
    'wind_spd',
    'slp',
    'elev_angle',
    'solar_rad',
    'pres',
    'snow_rate',
    'uv',
    'wind_dir',
    'description',
    'vis',
    'clouds',
    'timestamp_date',
    'timestamp_time'
]
'''
a6bee4ee4f1d4bd8a3a21e282664b6f7 - trolo4
a9e66359337349e4b302f117fa9fee6a - trolo5
1b602f74c0164cd4b24882198c8e367d - trolo6
8e8d9fff4675444caa732276d8725aa5 - trolo9
'''
api_key = 'a6bee4ee4f1d4bd8a3a21e282664b6f7'
sensor_ids = []
dates = []
sensor_names = []
with open('noise_sensors.txt', 'r') as sensors:
    for line in sensors.readlines():
        start_date = line.split(' - ')[2].split(': ')[1].split('-')
        dates.append(date(int(start_date[0]), int(start_date[1]), int(start_date[2])))
        sensor_ids.append(line.split(' - ')[0])
        sensor_names.append('_'.join(line.split(' - ')[1].lower().split(' ')))

for i in range(len(sensor_ids)):
    with open(f'{sensor_ids[i]}_{sensor_names[i]}.csv', 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        # writer.writeheader()
        print(f'WRITING TO {sensor_ids[i]}_{sensor_names[i]}')
        start_date = None
        end_date = None
        sensor_url = f'https://skopje.pulse.eco/rest/sensor/{sensor_ids[i]}'
        response = ast.literal_eval(requests.get(sensor_url).text)
        lat, log = response['position'].split(',')
        while True:
            if start_date is None:
                start_date = dates[i]
                if start_date.year == 2022 or (start_date.year == 2021 and start_date.month >= 3):
                    end_date = start_date + timedelta(days=28)
                else:
                    end_date = start_date + timedelta(days=28)
            else:
                start_date = end_date
                if start_date.year == 2022 and start_date.month == 3:
                    break
                if start_date.year == 2022 or (start_date.year == 2021 and start_date.month >= 3):
                    end_date = start_date + timedelta(days=28)
                else:
                    end_date = start_date + timedelta(days=28)
            weather_url = f'https://api.weatherbit.io/v2.0/history/subhourly?lat={lat}5&lon={log}&start_date={start_date}&end_date={end_date}&tz=local&key={api_key}'
            print(weather_url)
            weather_response = requests.get(weather_url)
            result = json.loads(weather_response.text)
            weather_dict = dict()
            for data in result['data']:
                for j in range(len(csv_columns)):
                    if j <= 2:
                        weather_dict[csv_columns[j]] = result[api_columns[j]]
                    if j > 2:
                        if api_columns[j] == 'description':
                            weather_dict[csv_columns[j]] = data['weather']['description']
                        elif api_columns[j] == 'timestamp_date':
                            weather_dict[csv_columns[j]] = data['timestamp_local'].split('T')[0]
                        elif api_columns[j] == 'timestamp_time':
                            weather_dict[csv_columns[j]] = data['timestamp_local'].split('T')[1]
                        else:
                            weather_dict[csv_columns[j]] = data[api_columns[j]]
                writer.writerow(weather_dict)
                print(weather_dict)
                print(weather_url)
            # file.write('\n')
            # print(weather_response.text[:100])
            # print(weather_url)
            # print(start_date, end_date)
            time.sleep(20)
