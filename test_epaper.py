import epaper1in54
from machine import SPI, Pin
import framebuf

# WeMos to Micropython ping mapping
D0 = 16
D1 = 5
D2 = 4
D3 = 0
D4 = 2
D5 = 14  # SPI SCK
D6 = 12  # SPI MISO
D7 = 13  # SPI MOSI
D8 = 15  # Slave select

# ePaper
CS_PIN = D0
DC_PIN = D1
RST_PIN = D2
BUSY_PIN = D3
# SCLK -> SPI SCK  (D5)
# SDI  -> SPI MOSI (D7)

# spi = SPI(3, SPI.MASTER, baudrate=2000000, polarity=0, phase=0)
# hardware SPI on ESP8266
spi = SPI(1, baudrate=80000000, polarity=0, phase=0)
cs = Pin(CS_PIN)
dc = Pin(DC_PIN)
rst = Pin(RST_PIN)
busy = Pin(BUSY_PIN)

display = epaper1in54.EPD(spi, cs, dc, rst, busy)
display.init()

DISPLAY_WIDTH = 200
DISPLAY_HEIGHT = 200

display.clear_frame_memory(0xFF)
display.display_frame()

buf = bytearray(DISPLAY_WIDTH * DISPLAY_HEIGHT // 8)
fb = framebuf.FrameBuffer(buf, 200, 200, framebuf.MONO_HLSB)
black = 0
white = 1
fb.fill(white)
fb.text('Hello World!', 16, 0, black)
fb.text('JENYA IS MY BUSECHKA', 16, 16, black)
display.set_frame_memory(buf, 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
display.display_frame()
