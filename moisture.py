from machine import ADC, Pin
from wemos import D8, A0


class SoilMoistureSensor:
    def __init__(self):
        self.adc = ADC(A0)
        # Powering the moisture sensor from a GPIO output pin
        # saves 5 mA during deep sleep.
        self.powerPin = Pin(D8, Pin.OUT)
        self.powerPin.on()

    def readValue(self):
        raw_value = self.adc.read()
        voltage = raw_value * 3.3 / 1024
        return {
            'soil_moisture_value': raw_value,
            'soil_moisture_voltage': voltage,
        }


if __name__ == '__main__':
    s = SoilMoistureSensor()
    v = s.readValue()
    print('Soil moisture sensor value: ', v)
