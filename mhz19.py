from wemos import D8
from machine import Pin
import time


class MHZ19:
    def __init__(self):
        self.pin = Pin(D8, Pin.IN)
        self.lastTimestamp = None
        self.lowDuration = None
        self.highDuration = None
        self.latestMeasurements = []

    def start(self):
        self.pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.callback)

    def callback(self, p):
        now = time.ticks_ms()
        if (self.lastTimestamp):
            duration = time.ticks_diff(time.ticks_ms(), self.lastTimestamp)
        else:
            duration = 0
        value = p.value()
        print('MH-Z19 interrupt handler', value, duration)
        self.lastTimestamp = now

        if value:
            self.lowDuration = duration
            if self.lowDuration and self.highDuration:
                co2 = self.calculateCo2Ppm(self.highDuration, self.lowDuration)
                print("instant CO2", co2)
                self.latestMeasurements.append(co2)
                if len(self.latestMeasurements) > 100:
                    self.latestMeasurements.pop(0)
        else:
            self.highDuration = duration
        self.lastTimestamp = now

    def calculateCo2Ppm(self, highDuration, lowDuration):
        return int(5000.0 * (1002.0 * highDuration - 2.0 * lowDuration) / 1000.0 / (highDuration + lowDuration))

    def getCo2(self):
        # get a median of the latest CO2 readings
        measurements = self.latestMeasurements
        self.latestMeasurements = []
        if len(measurements):
            measurements.sort()
            medianCo2 = measurements[len(measurements) // 2]
            print("CO2 median", medianCo2)
            return medianCo2
        else:
            print("WARN: no CO2 measurements found")
            return None


if __name__ == '__main__':
    mhz19 = MHZ19()
    mhz19.start()
    time.sleep(10)
    print('Median CO2', mhz19.getCo2())
