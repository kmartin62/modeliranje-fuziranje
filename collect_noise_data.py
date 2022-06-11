import requests
from datetime import timedelta, date
import time

sensor_id = 'f2c2ae38-27f3-4b98-a3a2-afce870b164e'
station = 'drachevo_kuzman'
file_name = f'{sensor_id}_{station}'
time_and_offset = 'T00:00:00%2b01:00'
# 2022-01-16
date_value = date(2022, 1, 16)

with open(f'{file_name}.json', 'w') as json_file:
    while not (date_value.year == 2022 and date_value.month == 3 and date_value.day <= 5):
        if date_value.year == 2022 and date_value.month == 3:
            break
        date_one_week = date_value + timedelta(days=7)
        url_link = f'https://skopje.pulse.eco/rest/dataRaw?sensorId={sensor_id}&from={str(date_value) + time_and_offset}&to={str(date_one_week) + time_and_offset}'
        date_value = date_one_week
        print(url_link)
        try:
            response = requests.get(url_link)
            json_file.write(response.text)
            json_file.write('\n')
        except:
            print(f'FAILED AT {url_link}')
        time.sleep(6)
