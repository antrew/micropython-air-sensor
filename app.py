import esp
import utime

import config
from config import WLAN_SSID, WLAN_PASSWORD, LOGSTASH_URL
from display import Display
from logstash import send_data_to_logstash
from sht30 import SHT30
from wlan import do_connect, disable_access_point

SEND_INTERVAL_SECONDS = 10

if hasattr(config, 'DEVICE_ID'):
    device_id = config.DEVICE_ID
else:
    device_id = 'mp-' + str(esp.flash_id())

sensor = ""

display = Display()


def setup():
    disable_access_point()
    do_connect(WLAN_SSID, WLAN_PASSWORD)
    global sensor
    sensor = SHT30()


def loop():
    temperature, humidity = sensor.measure()
    data = {
        'device_id': device_id,
        'temperature': temperature,
        'humidity': humidity
    }
    display.refresh(temperature, humidity)
    send_data_to_logstash(LOGSTASH_URL, data)


def run():
    setup()
    while True:
        loop()
        utime.sleep(SEND_INTERVAL_SECONDS)


if __name__ == '__main__':
    print('running once')
    # run once
    setup()
    loop()
