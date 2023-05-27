from umqtt.simple import MQTTClient


class MQTT:
    def __init__(self, mac, endpoint, port=8883):
        with open(f"keys/{mac}/private.pem") as key, open(f"keys/{mac}/certificate.pem") as cert:
            key_content = key.read()
            cert_content = cert.read()
            self.mqtt = MQTTClient(
                mac,
                endpoint,
                port=port,
                keepalive=10000,
                ssl=True,
                ssl_params={"cert": cert_content, "key": key_content},
            )

    def connect(self):
        self.mqtt.connect()

    def disconnect(self):
        self.mqtt.disconnect()

    def publish(self, topic, msg, qos=1, retain=False):
        # Publish a test MQTT message.
        self.mqtt.publish(topic=topic, msg=msg, qos=qos, retain=retain)
