# import modules
try:
   import terminal_options as term
except ImportError:
    print("The terminal_options.py file is not found!"); exit();

try:
   import scp_config as config
except ImportError:
   print(term.CRED + "Please copy scp_config_exemple.py to scp_config.py and configure appropriately !"  + term.CEND); exit();

try:
   import sensors
except ImportError:
   print(term.CRED + "The sensors.py file is not found!" + term.CEND); exit();

import time
import paho.mqtt.client as mqtt

#CONFIG
ENDPOINT = "iotmms" + config.scp_account_id + config.scp_landscape_host
ENDPOINT_CERTIFICATE = config.endpoint_certificate
DEVICE_ID = config.device_id
CLIENT_ID = DEVICE_ID
USERNAME = DEVICE_ID
PASSWORD = config.oauth_credentials_for_device
ENDPOINT_URL_PATH = "/com.sap.iotservices.mms/v1/api/ws/mqtt"
PUBLISH_TOPIC = "iot/data/" + DEVICE_ID
SUBSCIRPTION_TOPIC = "iot/push/" + DEVICE_ID

is_connected = False

# Function definition
def build_ram_info_message(messageID):
   """Return the formated JSON message for RAM INFOS"""
   infos = sensors.ram_info()
   mqtt_payload ='{"mode":"async", "messageType":"' + messageID + '","messages":[{'
   mqtt_payload = mqtt_payload + '"Total":' + str(infos[0])
   mqtt_payload = mqtt_payload + ', "Used":' + str(infos[1])
   mqtt_payload = mqtt_payload + ', "Free":' + str(infos[2])
   mqtt_payload = mqtt_payload + ', "timestamp":' + str(int(time.time()))
   mqtt_payload = mqtt_payload + '}]}'
   return mqtt_payload

def build_cpu_info_message(messageID):
   """Return the formated JSON message for CPU INFO"""
   infos = sensors.cpu_info()
   comp = sensors.cpu_info_comp()
   mqtt_payload ='{"mode":"async", "messageType":"' + messageID + '","messages":[{'
   mqtt_payload = mqtt_payload + '"CPU_Brand":' + str(infos[0])
   mqtt_payload = mqtt_payload + ', "CPU_Version":' + str(infos[1])
   mqtt_payload = mqtt_payload + ', "CPU_Hardware":' + str(infos[2])
   mqtt_payload = mqtt_payload + ', "CPU_Hz_actual":' + str(infos[3])
   mqtt_payload = mqtt_payload + ', "Owner":' + CLIENT_ID
   mqtt_payload = mqtt_payload + ', "Serial":' + str(comp[1])
   mqtt_payload = mqtt_payload + ', "Revision":' +  str(comp[0])
   mqtt_payload = mqtt_payload + ', "timestamp":' + str(int(time.time()))
   mqtt_payload = mqtt_payload + '}]}'
   return mqtt_payload

def build_cpu_use_message(messageID):
   """Return the formated JSON message for RAM USAGE"""
   mqtt_payload ='{"mode":"async", "messageType":"' + messageID + '","messages":[{'
   mqtt_payload = mqtt_payload + '"Temperature":' + str(sensors.cpu_temperature())
   mqtt_payload = mqtt_payload + ', "Usage_perc":' + str(sensors.cpu_use())
   mqtt_payload = mqtt_payload + ', "timestamp":' + str(int(time.time()))
   mqtt_payload = mqtt_payload + '}]}'
   return mqtt_payload

def build_disk_space_info_message(messageID):
   """Return the formated JSON message for DISK SPACE INFO"""
   infos = sensors.diskspace_info()
   mqtt_payload ='{"mode":"async", "messageType":"' + messageID + '","messages":[{'
   mqtt_payload = mqtt_payload + '"Total":' + str(infos[0])
   mqtt_payload = mqtt_payload + ', "Used":' + str(infos[1])
   mqtt_payload = mqtt_payload + ', "Available":' + str(infos[2])
   mqtt_payload = mqtt_payload + ', "Usage_perc":' + str(float(infos[3].replace("%", "")))
   mqtt_payload = mqtt_payload + ', "timestamp":' + str(int(time.time()))
   mqtt_payload = mqtt_payload + '}]}'
   return mqtt_payload

def dispatch_instruction(messageID):
   """Dispatch to the good message builder from incoming message ID"""
   message = None
   if messageID == config.CPU_INFO_MESSAGE_ID: message = build_cpu_info_message(messageID)
   elif messageID == config.CPU_USE_MESSAGE_ID: message = build_cpu_use_message(messageID)
   elif messageID == config.RAM_USE_MESSAGE_ID: message = build_ram_info_message(messageID)
   elif messageID == config.DISK_SPACE_INFO_MESSAGE_ID: message = build_disk_space_info_message(messageID)
   else: return False
   return message

def parse_message(payload, search):
   """Return the extracted data from the incoming payload message"""
   subString = payload[payload.find(search):]
   return(subString[len(search) + 3:subString.find(",") -1])

def on_connect(mqttc, obj, flags, rc):
   print(term.CBLUE + "on_connect   - rc: " + str(rc) + term.CEND)
   global is_connected
   is_connected = True
   mqttc.subscribe(SUBSCIRPTION_TOPIC, 0)

def on_message(client, userdata, message):
   stringload = str(message.payload.decode("utf-8"))
   print(term.CVIOLET + stringload + term.CEND)
   if parse_message(stringload, "messageType") == config.ASK_INFOS:
      message_back = dispatch_instruction(parse_message(stringload, "messageID"))
      if message_back != False:
         print(term.CYELLOW + message_back + term.CEND)
         client.publish(PUBLISH_TOPIC, message_back, qos=0)
      else:
         print(term.CRED + "Error: The Message ID required should be false" + term.CEND)

def on_publish(mqttc, obj, message_id):
   print(term.CBLUE + "on_publish   - message_id: " + str(message_id)  + term.CEND)

def on_subscribe(mqttc, obj, message_id, granted_qos):
   print(term.CBLUE + "on_subscribe - message_id: " + str(message_id) + " / qos: " + str(granted_qos)  + term.CEND)

def on_log(mqttc, obj, level, string):
   print(term.CGREEN + string + term.CEND)

mqttc = mqtt.Client(client_id=CLIENT_ID, transport='websockets')
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

mqttc.tls_set(ENDPOINT_CERTIFICATE)
mqttc.username_pw_set(USERNAME, PASSWORD)
mqttc.ws_set_options(ENDPOINT_URL_PATH)
mqttc.connect(ENDPOINT, 443, 60)
mqttc.loop_forever()
