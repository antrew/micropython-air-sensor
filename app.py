import esp
import ntptime
import utime

import config
from config import WLAN_SSID, WLAN_PASSWORD, LOGSTASH_URL
from logstash import send_data_to_logstash
from wlan import do_connect, disable_access_point


class App:
    def __init__(self):
        self.SEND_INTERVAL_SECONDS = 10

        if hasattr(config, 'DEVICE_ID'):
            self.device_id = config.DEVICE_ID
        else:
            self.device_id = 'mp-' + str(esp.flash_id())

        try:
            from display import Display
            self.display = Display()
        except ImportError:
            self.display = None

        try:
            from sht30 import SHT30
            self.sensor = SHT30()
        except ImportError:
            self.sensor = None

        disable_access_point()
        do_connect(WLAN_SSID, WLAN_PASSWORD)

        self.ntptimeWhenZero = 0

    def loop(self):
        data = {
            'device_id': self.device_id,
        }
        if self.sensor:
            temperature, humidity = self.sensor.measure()
            data['temperature'] = temperature
            data['humidity'] = humidity

        if self.ntptimeWhenZero <= 0:
            ntptime.settime()
            self.ntptimeWhenZero = 10
        self.ntptimeWhenZero -= 1

        if self.display:
            self.display.refresh(temperature, humidity)
        send_data_to_logstash(LOGSTASH_URL, data)

    def run(self):
        while True:
            self.loop()
            utime.sleep(self.SEND_INTERVAL_SECONDS)


if __name__ == '__main__':
    print('running once')
    # run once
    app = App()
    app.loop()
