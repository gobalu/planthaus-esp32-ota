import json

import ubinascii
from hdc1080 import HDC1080
from machine import Pin, SoftI2C, deepsleep, ADC
from moisture import Moisture
from mqtt import MQTT
from network import WLAN
from veml6040 import VEML6040
from wifi import Wifi


def main():
    try:
        wifi = Wifi()

        wifi.do_connect()

        if not wifi.is_connected():
            print("Failed to connect to wifi")

        mac = ubinascii.hexlify(WLAN().config("mac"), ":").decode()
        print("MAC: ", mac)

        mqtt = MQTT(mac, "a30gl9t17eaaq3-ats.iot.eu-west-1.amazonaws.com")
        print("MQTT: ", mqtt)

        mqtt.connect()
        i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)

        humidityTempSensor = HDC1080(i2c)
        lightSensor = VEML6040(i2c)
        moistureSensor = Moisture(Pin(36))
        battery = ADC(Pin(39), atten=ADC.ATTN_11DB)

        temperature = humidityTempSensor.read_temperature()
        print("Temperature: ", temperature)

        humidity = humidityTempSensor.read_humidity()
        print("Humidity: ", humidity)

        light = lightSensor.readRGB()
        print("Light: ", light)

        hsv = lightSensor.readHSV()
        print("HSV: ", hsv)

        moisture = 0
        for _ in range(10):
            moisture = moisture + moistureSensor.read_moisture_sensor()
        moisture = moisture / 10
        print("Moisture: ", moisture)

        batteryRaw = 0
        for _ in range(10):
            batteryRaw = batteryRaw + battery.read_u16()
        batteryRaw = batteryRaw / 10
        print("Battery Raw: ", batteryRaw)

        batteryVoltage = batteryRaw / 65535 * 3.3 * 2 * 1.076
        print("Battery Voltage: ", batteryVoltage)

        data = {
            "thing": mac,
            "THS": {
                "temperature": temperature,
                "humidity": humidity,
            },
            "ALS": {
                "light": light,
                "hsv": hsv,
            },
            "Moisture": moisture,
            "Battery": batteryVoltage,
        }
        print("Data: ", data)

        mqtt.publish("sensor", json.dumps(data))
        mqtt.disconnect()
        print("Temperture: ", humidityTempSensor.read_temperature())
        print("Humidity: ", humidityTempSensor.read_humidity())
        print("Light: ", lightSensor.readRGB())
        print("HSV: ", lightSensor.readHSV())
        print("Moisture: ", moistureSensor.read_moisture_sensor())
    except:
        print("Exception: ", e)
    finally:
        deepsleep(30000)


if __name__ == "__main__":
    main()
