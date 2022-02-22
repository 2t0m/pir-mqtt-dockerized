import logging
import os
import time
import json
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from RPi import GPIO

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
PIN = int(os.getenv('GPIO_PIN'), 17)
SCAN_INTERVAL = float(os.getenv('SCAN_INTERVAL', 100))
SENSOR_NAME = os.getenv('SENSOR_NAME', "pir")
MQTT_CONFIG = "homeassistant/binary_sensor/"+SENSOR_NAME+"/config";
MQTT_STATE = "homeassistant/binary_sensor/"+SENSOR_NAME+"/state"
MQTT_HOSTNAME = os.getenv("MQTT_HOSTNAME", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TIMEOUT = int(os.getenv("MQTT_TIMEOUT", 60))
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "pir-sensor-mqtt")
MQTT_CLEAN_SESSION = os.getenv("CLIENT_CLEAN_SESSION", False)
MQTT_TLS_INSECURE = os.getenv("CLIENT_TLS_INSECURE", True)
MQTT_CLIENT_QOS = int(os.getenv("CLIENT_QOS", 0))
MQTT_USERNAME = os.getenv('MQTT_USERNAME', None)
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', None)


def configure_logging():

    level_map={
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'WARN': logging.WARNING,
        'ERROR': logging.ERROR
    }

    log_level=level_map.get(LOG_LEVEL, "Unsupported log level provided!")
    logging.basicConfig(level=log_level)


def on_connect(client, userdata, flags, rc):
    logging.info("Connected to the MQTT broker!")


def on_disconnect(client, userdata, flags, rc):
    logging.warn(f"Disconnected from the MQTT broker. End state - '{rc}'")


GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)

configure_logging()

logging.info("Initializing PIR "+SENSOR_NAME+" on port "+str(PIN)+" with interval of "+str(SCAN_INTERVAL)+"ms.")

if MQTT_HOSTNAME is None or MQTT_PORT is None:
    logging.error("Could not acquire MQTT broker connection parameters...")
    exit(1)

client = mqtt.Client(MQTT_CLIENT_ID, MQTT_CLEAN_SESSION)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.connect(MQTT_HOSTNAME, MQTT_PORT, MQTT_TIMEOUT)

client.loop_start()

pir_data_conf = {"name": "PIR Sensor", "unique_id": SENSOR_NAME, "device_class": "motion", "state_topic": MQTT_STATE}

logging.info("Publishing default to config "+MQTT_CONFIG+" and state "+MQTT_STATE)

def motion_detected(channel):
    logging.info('Motion On')
    client.publish(MQTT_CONFIG, json.dumps(pir_data_conf))
    client.publish(MQTT_STATE, "ON")
    time.sleep(4)
    logging.info('Motion Off')
    client.publish(MQTT_STATE, "OFF")

logging.info("Successfully initialized application! Let's try to read the sensor...")
    
try:
    GPIO.add_event_detect(PIN, GPIO.RISING, callback=motion_detected, bouncetime=300)
    while True:
        client.publish(MQTT_CONFIG, json.dumps(pir_data_conf))
        time.sleep(10)
except Exception as e:
        logging.error(f"Something went wrong and this shouldn't happen... Details: {e}")

GPIO.cleanup()
client.loop_stop()
client.disconnect()
