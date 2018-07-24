# import modules
import sys
import time
import paho.mqtt.client as mqtt

# set credentials
RASPBERRY_MESSAGE_ID = "9ce48c3c6d6a3572b1a3"
MQTT_BROKER_HOST = "iot.eclipse.org"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "iot/data/iotmmss0018463047trial/v1/cfad3c57-8bce-4349-9d5c-59dfa5da7410"

# functions
def on_connect(client, userdata, flags, rc):
    print("Connected with code: " + str(rc))

# open the mqtt connexion
client = mqtt.Client()
client.on_connect = on_connect
client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)

# deliver the message
MESSAGE_STR = "Hello Sap Cloud Platform via MQTT Protocol"
messageJSON = {
	"mode":"async",
	"messageType": RASPBERRY_MESSAGE_ID,
	"messages":[
		{
			"timestamp": int(time.time()),
			"message": MESSAGE_STR
		}
	]
}

client.publish(MQTT_TOPIC, payload=str(messageJSON))

sys.exit(0)
