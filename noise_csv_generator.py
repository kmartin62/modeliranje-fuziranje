import ast
import csv
import os

csv_columns = ['sensor_id', 'date', 'time', 'lat', 'log', 'temperature', 'noise', 'noise_dba', 'pm10', 'humidity',
               'pm25', 'gasResistance', 'pressure']

list_files = os.listdir('skopje_noise_for_generator/')
for file in list_files:
    file_path = f'skopje_noise_json/{file}'
    csv_file_path = f'{file.split(".")[0]}.csv'
    print(file_path, csv_file_path)
    with open(file_path) as f:
        try:
            with open(csv_file_path, 'a', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
                writer.writeheader()
                for line in f:
                    list_line = ast.literal_eval(line)
                    dict_line = dict()
                    for elem in list_line:
                        if elem['type'] in dict_line:
                            dict_line['sensor_id'] = elem['sensorId']
                            dict_line['date'] = elem['stamp'].split('T')[0]
                            dict_line['time'] = elem['stamp'].split('T')[1].split('+')[0]
                            dict_line['lat'] = elem['position'].split(',')[0]
                            dict_line['log'] = elem['position'].split(',')[1]
                            writer.writerow(dict_line)
                            # print(dict_line)
                            dict_line = dict()
                        dict_line[elem['type']] = elem['value']
            print('finish')
        except IOError:
            print("I/O Error")
