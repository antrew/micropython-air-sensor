# Monitor Air Quality with ESP8266+MicroPython and Elastic Stack

This project does the following:
* Read temperature and humidity from an SHT30 sensor
* Send the read values to Logstash with an HTTP POST request with JSON payload

## Prerequisites

### Hardware

* WeMos ESP8266
* WeMos SHT30

### Build tools

You will need to install the following tools to flash this project to an ESP8266 board:

* adafruit-ampy - a tool to interact with a MicroPython flashed board:
    ```
    pip3 install adafruit-ampy
    ```

### Flashing MicroPython

If you haven't already done it,
follow this tutorial to flash MicroPython to your ESP8266: 
http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html

## Uploading scripts

### Uploading scripts

1. Set your WLAN SSID and password in config.py
2. Upload base scripts to your MicroPython board:

```bash
# modify the path to the USB serial port if necessary
export AMPY_PORT=/dev/ttyUSB0
ampy put config.py
ampy put logstash.py
ampy put wlan.py
ampy put app.py
ampy put main.py
```

3. Upload optional modules (only those that are actually connected):

```bash
ampy put sht30.py
ampy put bmp180.py
ampy put display.py
ampy put mhz19.py
ampy put moisture.py
```

### Testing parts

#### Testing SHT30

```bash
ampy run test_sht30.py
```

#### Testing BMP180

```bash
ampy run test_bmp180.py
```

#### Testing WLAN

```bash
ampy run test_wlan.py
```

#### Testing Logstash

```bash
ampy run test_logstash.py
```

#### Serial console

```
miniterm.py --raw /dev/ttyUSB0 115200
```

## Acknowledgements

* sht30.py is taken from here: https://github.com/rsc1975/micropython-sht30
* bmp180.py is taken from here: https://github.com/micropython-IMU/micropython-bmp180
* urequests.py is taken from here: https://github.com/micropython/micropython-lib
