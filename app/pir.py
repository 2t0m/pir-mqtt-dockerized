import logging
import os
import time
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from RPi import GPIO

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] pir: %(message)s', )

PIN = int(os.getenv('GPIO_PIN'))
SCAN_INTERVAL = int(os.getenv('SCAN_INTERVAL'))
SENSOR_NAME = os.getenv('SENSOR_NAME')
MQTT_HOST = os.getenv('MQTT_HOST')
MQTT_HOST = os.getenv('MQTT_HOST')
MQTT_USER = os.getenv('MQTT_USER')
MQTT_PASS = os.getenv('MQTT_PASS')

logging.info("Initializing PIR "+SENSOR_NAME+" on port "+str(PIN)+" with interval of "+str(SCAN_INTERVAL)+"ms.")

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)

auth = {
  'username': MQTT_USER,
  'password': MQTT_PASS
}

publish.single("homeassistant/binary_sensor/"+SENSOR_NAME+"/config",
      payload='{"name": "PIR Sensor", "unique_id": "+SENSOR_NAME+", "object_id": "+SENSOR_NAME+", "device_class": "motion", "state_topic": "homeassistant/binary_sensor/"+SENSOR_NAME+"/state", "retain": "true"}',
      hostname=MQTT_HOST,
      client_id="pir-mqtt",
      auth=auth,
      port=1883,
      protocol=mqtt.MQTTv311)

def my_callback(channel):
    logging.info('Motion On')
    publish.single("homeassistant/binary_sensor/"+SENSOR_NAME+"/state",
      payload="ON",
      hostname=MQTT_HOST,
      client_id="pir-mqtt",
      auth=auth,
      port=1883,
      protocol=mqtt.MQTTv311)
    time.sleep(4)
    logging.info('Motion Off')
    publish.single("homeassistant/binary_sensor/"+SENSOR_NAME+"/state",
      payload="OFF",
      hostname=MQTT_HOST,
      client_id="pir-mqtt",
      auth=auth,
      port=1883,
      protocol=mqtt.MQTTv311)
    
try:
    GPIO.add_event_detect(PIN, GPIO.RISING, callback=my_callback)
    while True:
        time.sleep(SCAN_INTERVAL)
except KeyboardInterrupt:
    logging.info("Finish...")
GPIO.cleanup()
