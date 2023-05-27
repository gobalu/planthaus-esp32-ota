from machine import Timer
import bluetooth
import time

BLE_MSG = ""


class ESP32_BLE():
    def __init__(self, name):
        self.timer1 = Timer(0)
        self.name = name
        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.ble.config(gap_name=name)
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.ble.gatt_write(self.rx, bytes(100))
        self.advertiser() 
        self.ok = 0
        self.ble_msg = ""

    def disconnected(self):
        print("Disconnected")

    def register(self):
        service_uuid = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        reader_uuid = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        sender_uuid = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'

        services = (
            (
                bluetooth.UUID(service_uuid),
                (
                    (bluetooth.UUID(sender_uuid), bluetooth.FLAG_NOTIFY),
                    (bluetooth.UUID(reader_uuid), bluetooth.FLAG_WRITE),
                )
            ),
        )

        ((self.tx, self.rx,), ) = self.ble.gatt_register_services(services)

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = bytearray('\x02\x01\x02') + \
            bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)

    def ble_irq(self, event, _data):

        if event == 1:  # Connected event
            self.connected()
        elif event == 2:
            if self.ok == 0:
                self.advertiser()
                self.disconnected()
        elif event == 3:  # Receive data
            buffer = self.ble.gatts_read(self.rx)
            self.ble_msg = buffer.decode('UTF-8').strip()
            self.wifi_get_data()

    def connected(self):
        self.timer1.deinit()

    def _store_wifi_config(self):
        if len(self.ble_msg) > 0:
            with open('wifi.txt', 'w+') as f:
                f.write(self.ble_msg)

    def disable_ble(self):
        self.ble.active(False)


if __name__ == "__main__":
    ble = ESP32_BLE("PlantHaus")

    while True:
        if ble.ok:  # 如果WiFi已连接，进行xxxxx
            time.sleep(1)