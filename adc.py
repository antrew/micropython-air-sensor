from machine import ADC, Pin

from module import Module

ESP32_FIRST_ADC_PIN = 32
ESP32_LAST_ADC_PIN = 39


class Battery(Module):
    #     def __init__(self):
    #         self.adc = ADC(A0)
    #
    #     def getVoltage(self, raw_value):
    #         return raw_value \
    #                * (RESISTOR_GND_ADC + RESISTOR_ADC_A0 + RESISTOR_A0_BATTERY) \
    #                / RESISTOR_GND_ADC \
    #                / 1024
    #
    #     def readValue(self):
    #         raw_value = self.adc.read()
    #         voltage = self.getVoltage(raw_value)
    #         return {
    #             'battery_adc_raw': raw_value,
    #             'battery_voltage': voltage,
    #         }
    #
    #     def getDisplayLines(self, data):
    #         return [
    #             'Battery ADC raw: {}'.format(data['battery_adc_raw']),
    #             'Battery voltage: {} V'.format(data['battery_voltage'])
    #         ]

    def scan(self):
        for pin in range(ESP32_FIRST_ADC_PIN, ESP32_LAST_ADC_PIN + 1):
            adc = ADC(Pin(pin))
            adc.atten(ADC.ATTN_11DB)
            value = adc.read()
            voltage = value * 3.6 / 4096
            print('pin: {} value: {} voltage: {}'.format(pin, value, voltage))


if __name__ == '__main__':
    Battery().scan()
