from machine import ADC, Pin

from module import Module


class Moisture(Module):
    def __init__(self):
        self.adc = ADC(Pin(32))
        self.adc.atten(ADC.ATTN_11DB)

    def readValue(self):
        raw_value = self.adc.read()
        voltage = raw_value / 4096 * 3.6
        return {
            'moisture_adc_raw': raw_value,
            'moisture_voltage': voltage,
        }

    def getDisplayLines(self, data):
        return [
            'Moisture ADC raw: {}'.format(data['moisture_adc_raw']),
            'Moisture voltage: {} V'.format(data['moisture_voltage'])
        ]


if __name__ == '__main__':
    Moisture().test()
