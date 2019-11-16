import framebuf
import utime
from machine import SPI, Pin

import epaper1in54
from wemos import D1, D2, D6, D8


class Epaper:
    def __init__(self):
        self.display = None
        self.try_init()

    def try_init(self):
        # ePaper
        CS_PIN = D2
        DC_PIN = D1
        RST_PIN = D8
        BUSY_PIN = D6
        # SCLK -> SPI SCK  (D5)
        # SDI  -> SPI MOSI (D7)

        # spi = SPI(3, SPI.MASTER, baudrate=2000000, polarity=0, phase=0)
        # hardware SPI on ESP8266
        spi = SPI(1, baudrate=80000000, polarity=0, phase=0)
        cs = Pin(CS_PIN)
        dc = Pin(DC_PIN)
        rst = Pin(RST_PIN)
        busy = Pin(BUSY_PIN)

        print('Initializing epaper...')

        self.display = epaper1in54.EPD(spi, cs, dc, rst, busy)
        self.display.init()

        print('Done initializing epaper')
        self.DISPLAY_WIDTH = 200
        self.DISPLAY_HEIGHT = 200
        self.LINE_HEIGHT = 16

    def refresh(self, display_lines):
        t = utime.localtime()

        self.display.clear_frame_memory(0xFF)
        self.display.display_frame()

        buf = bytearray(self.DISPLAY_WIDTH * self.DISPLAY_HEIGHT // 8)
        fb = framebuf.FrameBuffer(buf, 200, 200, framebuf.MONO_HLSB)
        black = 0
        white = 1
        fb.fill(white)
        fb.text('Hello World!', 16, 0 * self.LINE_HEIGHT, black)

        fb.text('{:02d}:{:02d}:{:02d}'.format(t[3], t[4], t[5]), 0, 2 * self.LINE_HEIGHT, black)
        offset_y = 3 * self.LINE_HEIGHT
        for line in display_lines:
            fb.text(line, 0, offset_y, black)
            offset_y += self.LINE_HEIGHT

        self.display.set_frame_memory(buf, 0, 0, self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT)
        self.display.display_frame()


if __name__ == '__main__':
    import ntptime
    import time

    ntptime.settime()
    # print('Hello!')
    epaper = Epaper()
    for _ in range(5):
        epaper.refresh(['T 23.8464', 'RH 36.0967'])
        time.sleep(5)
