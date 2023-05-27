import os
import time

import network


class Wifi:
    wifi_connection_details = "WIFI:S:google wifi;T:WPA;P:ryqrdkrf;H:false;;"
    sta_if = network.WLAN(network.STA_IF)
    debug = True

    def __init__(self):
        if "wifi.txt" in os.listdir("/"):
            with open("/wifi.txt", "r") as f:
                wifi_file_contents = f.read()
                # Convert format "WIFI:S:google wifi;T:WPA;P:ryqrdkrf;H:false;;" to dict
                wifi_creds = wifi_file_contents[1:-1].split("WIFI:")[1]
                print(wifi_creds)
                self.wifi_connection_details = dict(
                    [tuple(x.split(":")) for x in wifi_creds.split(";") if x]
                )
        else:
            print("No wifi.txt file found, using default wifi connection details")

    def do_connect(self):
        if not self.wifi_connection_details:
            print("No wifi connection details found")
            return
        if not self.sta_if.isconnected():
            print("connecting to network...", self.wifi_connection_details)
            self.sta_if.active(True)
            self.sta_if.connect(
                self.wifi_connection_details["S"], self.wifi_connection_details["P"]
            )

            # Wait while connecting or timeout after 30 seconds
            for _ in range(30):
                if self.sta_if.isconnected():
                    break
                time.sleep(1)

        if self.debug and self.sta_if.isconnected():
            print("network config:", self.sta_if.ifconfig())
        elif not self.debug and not self.sta_if.isconnected():
            print("Failed to connect to wifi")

    def is_connected(self):
        return self.sta_if.isconnected()
