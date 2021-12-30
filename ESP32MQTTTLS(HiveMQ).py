from simple import MQTTClient
import Wifi
import machine, time
import ujson
from machine import ADC

Wifi.connectWifi()
# with certificates we could not get it worked
# but after many tries, adding ssl_params={"server_hostname": "xxxxxxxxxxx.s1.eu.hivemq.cloud.s1.eu.hivemq.cloud"}
# has solved the connection problem. 
mqtt_client = MQTTClient(
            "esp-home1",
            "xxxxxxxxxxx.s1.eu.hivemq.cloud",
            port=8883,
            user="xxxxxxx",
            password="xxxxxxx",
            ssl=True,
            keepalive=60*60,
            ssl_params={"server_hostname": "xxxxxxxxxxx.s1.eu.hivemq.cloud.s1.eu.hivemq.cloud"}
        )
print('Connecting to HiveMQ...')

def sub_cb(topic, msg):
  print((topic, msg))

mqtt_client.set_callback(sub_cb)
mqtt_client.connect()
print("Connected....")
mqtt_client.subscribe("Commands")
 
def callbackfunction(arg):
    mqtt_client.publish("Status", "Ok")
    
from machine import Timer
tim = Timer(-1)
tim.init(period=5000, mode=Timer.PERIODIC, callback=callbackfunction)



while True:
  try:
    mqtt_client.check_msg() 
      
  except OSError as e:
    print(e)
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

