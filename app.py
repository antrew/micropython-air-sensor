import esp
import ntptime
import utime

import config
from config import WLAN_SSID, WLAN_PASSWORD, LOGSTASH_URL
from logstash import send_data_to_logstash
from wlan import do_connect, disable_access_point

DEFAULT_SEND_INTERVAL_SECONDS = 60


class App:
    def __init__(self):

        if hasattr(config, 'DEVICE_ID'):
            self.device_id = config.DEVICE_ID
        else:
            self.device_id = 'mp-' + str(esp.flash_id())

        if hasattr(config, 'SEND_INTERVAL_SECONDS'):
            self.sendIntervalSeconds = config.SEND_INTERVAL_SECONDS
        else:
            self.sendIntervalSeconds = DEFAULT_SEND_INTERVAL_SECONDS

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

        try:
            from moisture import SoilMoistureSensor
            self.soilMoistureSensor = SoilMoistureSensor()
        except ImportError:
            self.soilMoistureSensor = None

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

        if self.soilMoistureSensor:
            soilMoisture = self.soilMoistureSensor.readValue()
            data.update(soilMoisture)

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
            utime.sleep(self.sendIntervalSeconds)


if __name__ == '__main__':
    print('running once')
    # run once
    app = App()
    app.loop()
