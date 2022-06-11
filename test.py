lista = []
lista.extend(range(1, 3))
file_name = '60aa65c6-b7c4-4aae-8769-5dbcba356b5d_avtokomanda'
for i in range(len(lista)):
    with open('skopje_weather_json/' + file_name + '_' + str(lista[i]) + '.json', 'w') as f:
        print(file_name + '_' + str(lista[i]) + '.json')
