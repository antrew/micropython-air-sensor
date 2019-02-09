from machine import ADC


class SoilMoistureSensor:
    def __init__(self):
        self.adc = ADC(0)

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
