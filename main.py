import esp
import utime

from config import WLAN_SSID, WLAN_PASSWORD, LOGSTASH_URL
from logstash import send_data_to_logstash
from sht30 import SHT30
from wlan import do_connect

SEND_INTERVAL_SECONDS = 10
device_id = esp.flash_id()

sensor = ""


def setup():
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
    send_data_to_logstash(LOGSTASH_URL, data)
    utime.sleep(SEND_INTERVAL_SECONDS)


setup()

while True:
    loop()
