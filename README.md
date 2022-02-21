# pir-mqtt-dockerized
pir-mqtt-dockerized for HomeAssistant

## Running docker container

### Using docker-compose
Requires docker-compose to be [installed on your Raspberry Pi](https://dev.to/rohansawant/installing-docker-and-docker-compose-on-the-raspberry-pi-in-5-simple-steps-3mgl).

Set a available configuration for the command in the `Available variables` section below and add the following to your `docker-compose.yml` file and run the `docker-compose up -d` command.
```
version: '3.3'
services:
  pir-mqtt:
    build: .
    image: pir-mqtt
    container_name: pir-mqtt
    privileged: true
    restart: unless-stopped
    environment:
      GPIO_PIN: 7
      SCAN_INTERVAL: 100
      MQTT_HOST: localhost
      MQTT_USER: ''
      MQTT_PASS: ''
```

### Available variables

- `GPIO_PIN` - an integer for the Raspberry Pi pin to which the PIR Data pin is connected to.
- `SCAN_INTERVAL` - an integer in milliseconds.
- `MQTT_HOST` - the hostname or IP address of the MQTT broker to which the client should connect to.
- `MQTT_USER` - Set a username for broker authentication.
- `MQTT_PASS` - Set a password for broker authentication.
