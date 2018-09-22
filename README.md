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

```bash
export AMPY_PORT=/dev/ttyUSB0
ampy put sht30.py
```

### Testing parts

#### Testing SHT30

```bash
ampy run test_sht30.py
```

## Acknowledgements

* sht30.py is taken from here: https://github.com/rsc1975/micropython-sht30
