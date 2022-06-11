import ast
import json
import os
import csv

file = 'drachevo_kuzman'
root_path = f'skopje_weather_json/{file}'

list_files = os.listdir(root_path)

csv_columns = ['timezone', 'country_code', 'station_id', 'relative_humidity', 'wind_speed', 'part_of_day',
               'sea_level_pressure', 'solar_elevation_angle', 'solar_radiation', 'pressure', 'snow',
               'uv', 'wind_direction', 'weather_description', 'visibility', 'clouds', 'date', 'time']

api_columns = [
    'timezone',
    'country_code',
    'station_id',
    'rh',
    'wind_spd',
    'pod',
    'slp',
    'elev_angle',
    'solar_rad',
    'pres',
    'snow',
    'uv',
    'wind_dir',
    'description',
    'vis',
    'clouds',
    'timestamp_date',
    'timestamp_time'
]
# 'weather['description']'

for elem in list_files:
    with open(root_path + '/' + elem, encoding='utf-8') as f:
        result = json.loads(f.read())
        weather_dict = dict()
        # print(result)
        with open(f'{file}.csv', 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
            writer.writeheader()
            for data in result['data']:
                for i in range(len(csv_columns)):
                    if i <= 2:
                        weather_dict[csv_columns[i]] = result[api_columns[i]]
                    if i > 2:
                        if api_columns[i] == 'description':
                            weather_dict[csv_columns[i]] = data['weather']['description']
                        elif api_columns[i] == 'timestamp_date':
                            weather_dict[csv_columns[i]] = data['timestamp_local'].split('T')[0]
                        elif api_columns[i] == 'timestamp_time':
                            weather_dict[csv_columns[i]] = data['timestamp_local'].split('T')[1]
                        else:
                            weather_dict[csv_columns[i]] = data[api_columns[i]]
                writer.writerow(weather_dict)
                print(weather_dict)
