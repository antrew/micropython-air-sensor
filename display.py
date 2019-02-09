import ssd1306
from machine import I2C, Pin
import utime


class Display:
    def __init__(self):
        self.i2c = I2C(-1, Pin(5), Pin(4))
        self.display = None
        self.try_init()

    def try_init(self):
        print('try_init i2c devices:', self.i2c.scan())
        try:
            self.display = ssd1306.SSD1306_I2C(64, 48, self.i2c, addr=0x3c)
        except Exception as e:
            print('Error initializing display', e)
            print('i2c devices:', self.i2c.scan())

    def refresh(self, display_lines):
        print('refresh i2c devices:', self.i2c.scan())
        if not self.display:
            self.try_init()
        if not self.display:
            return
        t = utime.localtime()
        self.display.fill(0)
        self.display.text('{:02d}:{:02d}:{:02d}'.format(t[3], t[4], t[5]), 0, 0)
        offset_y = 8
        for line in display_lines:
            self.display.text(line, 0, offset_y)
            offset_y += 8
        try:
            self.display.show()
        except Exception as e:
            print('Error showing display', e)


if __name__ == '__main__':
    import ntptime
    import time

    ntptime.settime()
    # print('Hello!')
    display = Display()
    for _ in range(5):
        display.refresh(['T 23.8464', 'RH 36.0967'])
        time.sleep(1)
