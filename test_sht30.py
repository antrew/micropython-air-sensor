from sht30 import SHT30, SHT30Error

sensor = SHT30()

if sensor.is_present():
    try:
        temperature, humidity = sensor.measure()
        print('SHT30: Temperature:', temperature, 'ºC, RH:', humidity, '%')
    except SHT30Error as e:
        print('Error reading SHT30 sensor:', e)
else:
    print('SHT30 sensor is not connected')
