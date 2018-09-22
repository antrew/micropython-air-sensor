from bmp180 import BMP180
from machine import I2C, Pin  # create an I2C bus object accordingly to the port you are using

i2c = I2C(-1, Pin(5), Pin(4), freq=100000)

try:
    bmp180 = BMP180(i2c)
    bmp180.oversample_sett = 2
    bmp180.baseline = 101325

    temp = bmp180.temperature
    p = bmp180.pressure
    altitude = bmp180.altitude
    print('BMP180: Temperature:', temp, 'Pressure:', p, 'Altitude:', altitude)
except OSError as e:
    print('Error reading BMP180:', e)
