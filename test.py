from machine import ADC, Pin

# ADC pins are 32 to 39

for p in range(32, 39 + 1):
    adc = ADC(Pin(p))
    adc.atten(ADC.ATTN_11DB)
    v = adc.read()
    print('ADC {} value: {}'.format(p, v))
