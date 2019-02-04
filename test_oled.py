import ssd1306
import network
from machine import I2C, Pin
import utime

i2c = I2C(-1, Pin(5), Pin(4))

print(i2c.scan())

display = ssd1306.SSD1306_I2C(64, 48, i2c, addr=0x3c)

# [60, 69, 119]
# 60 == 0x3c == display

display.fill(0)

import ntptime
ntptime.settime()

t = utime.localtime()
display.text('{:02d}:{:02d}:{:02d}'.format(t[3], t[4], t[5]), 0,0)

w = network.WLAN(network.STA_IF)
if w.active():
    active = 'A'
else:
    active = '_'
if (w.isconnected()):
    connected = 'C'
else:
    connected = '_'
display.text('{}{}'.format(active, connected), 0, 16)
addr = w.ifconfig()[0]
a = addr.split('.')
display.text('{}.{}'.format(a[0], a[1]), 0, 24)
display.text('.{}.{}'.format(a[2], a[3]), 0, 32)

display.show()
