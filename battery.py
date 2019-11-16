from machine import ADC

from module import Module
from wemos import A0

# GND -[100k]- ADC -[220k]- A0 -[1000]- BAT+
# all values in kOhm
RESISTOR_GND_ADC = 100
RESISTOR_ADC_A0 = 220
RESISTOR_A0_BATTERY = 1000


class Battery(Module):
    def __init__(self):
        self.adc = ADC(A0)

    def getVoltage(self, raw_value):
        return raw_value \
               * (RESISTOR_GND_ADC + RESISTOR_ADC_A0 + RESISTOR_A0_BATTERY) \
               / RESISTOR_GND_ADC \
               / 1024

    def readValue(self):
        raw_value = self.adc.read()
        voltage = self.getVoltage(raw_value)
        return {
            'battery_adc_raw': raw_value,
            'battery_voltage': voltage,
        }

    def getDisplayLines(self, data):
        return [
            'Battery ADC raw: {}'.format(data['battery_adc_raw']),
            'Battery voltage: {} V'.format(data['battery_voltage'])
        ]


if __name__ == '__main__':
    Battery().test()
