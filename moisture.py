from machine import ADC

class Moisture:
    def __init__(self, pin):
        self.adc = ADC(pin, atten=ADC.ATTN_11DB)

    def read_moisture_sensor(self):
        """ Read the moisture sensor """
        return self.adc.read_u16()