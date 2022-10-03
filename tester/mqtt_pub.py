import paho.mqtt.client as mqtt
from datetime import datetime
import sys
import time

client = mqtt.Client()
if client.connect('localhost',1883, 60) != 0:
    print('Could not connect to mqtt broker')
    sys.exit(-1)

topic = '/exvis/sub/test'
for i in range(30):
    ms = 'Hello world ' + str(datetime.now())
    print(f'Topic: {topic} -> msg: {ms}')
    client.publish(topic, ms, 0)
    time.sleep(0.1)
client.disconnect()