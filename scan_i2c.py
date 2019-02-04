from machine import I2C, Pin

i2c = I2C(-1, Pin(5), Pin(4))
print(i2c.scan())
