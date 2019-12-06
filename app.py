import esp
import uos
import machine
import ntptime
import utime

import config
from config import WLAN_SSID, WLAN_PASSWORD
from wlan import do_connect, disable_access_point

DEFAULT_SEND_INTERVAL_SECONDS = 60

MODULES = [
    'battery.Battery',
    'moisture32.Moisture',
]


class App:
    def init(self):
        if hasattr(config, 'DEVICE_ID'):
            self.device_id = config.DEVICE_ID
        else:
            self.device_id = 'mp-' + str(esp.flash_id())

        if hasattr(config, 'SEND_INTERVAL_SECONDS'):
            self.sendIntervalSeconds = config.SEND_INTERVAL_SECONDS
        else:
            self.sendIntervalSeconds = DEFAULT_SEND_INTERVAL_SECONDS

        self.loadedModules = []
        for moduleName in MODULES:
            print('Trying to import module ' + moduleName)
            try:
                [packageName, className] = moduleName.split('.')
                package = __import__(packageName)
                ModuleClass = getattr(package, className)
                module = ModuleClass()
                self.loadedModules.append(module)
                print('Imported module ' + moduleName)
            except ImportError as error:
                print("Module {} could not be imported".format(moduleName))

        try:
            from logstash import Logstash
            self.logstash = Logstash()
        except ImportError:
            self.logstash = None

        try:
            from display import Display
            self.display = Display()
        except ImportError:
            self.display = None

        try:
            from epaper import Epaper
            self.epaper = Epaper()
        except ImportError:
            self.epaper = None

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

        try:
            from mhz19 import MHZ19
            self.mhz19 = MHZ19()
            self.mhz19.start()
        except ImportError:
            self.mhz19 = None

        disable_access_point()
        do_connect(WLAN_SSID, WLAN_PASSWORD)

        ntptime.settime()
        self.ntptimeWhenZero = 10

    def loop(self):
        data = {
            'device_id': self.device_id,
        }
        display_lines = []

        for module in self.loadedModules:
            moduleData = module.readValue()
            moduleDisplayLines = module.getDisplayLines(moduleData)
            data.update(moduleData)
            display_lines.extend(moduleDisplayLines)

        if self.sensor:
            temperature, humidity = self.sensor.measure()
            data['temperature'] = temperature
            data['humidity'] = humidity
            display_lines.append('T  {0:.1f}°C'.format(temperature))
            display_lines.append('RH {0:.1f}%'.format(humidity))

        if self.soilMoistureSensor:
            soilMoisture = self.soilMoistureSensor.readValue()
            data.update(soilMoisture)

        if self.mhz19:
            co2 = self.mhz19.getCo2()
            if co2:
                data['co2'] = co2
                display_lines.append('CO2 {}'.format(co2))

        if self.ntptimeWhenZero <= 0:
            ntptime.settime()
            self.ntptimeWhenZero = 10
        self.ntptimeWhenZero -= 1

        if self.display:
            self.display.refresh(display_lines)

        if self.epaper:
            self.epaper.refresh(display_lines)

        if self.logstash:
            self.logstash.send_data(data)

    def run(self):
        while True:
            self.loop()
            utime.sleep(self.sendIntervalSeconds)

    def deepsleep(self):
        print('Going to deep sleep for {} seconds'.format(self.sendIntervalSeconds))
        if uos.uname().sysname == 'esp32':
            # ESP32
            machine.deepsleep(self.sendIntervalSeconds * 1000)
        else:
            # ESP8266

            # configure RTC.ALARM0 to be able to wake the device
            rtc = machine.RTC()
            rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

            # set RTC.ALARM0 to fire after 10 seconds (waking the device)
            rtc.alarm(rtc.ALARM0, self.sendIntervalSeconds * 1000)

            # put the device to sleep
            machine.deepsleep()


if __name__ == '__main__':
    print('running once')
    # run once
    app = App()
    app.loop()
