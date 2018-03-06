import paho.mqtt.client as MQTT
import time
import json


class MyPublisher:
    def __init__(self, clientID):
        self.clientID = clientID

        # create an instance of paho.mqtt.client
        self.mqtt_client = MQTT.Client(self.clientID, True)
        # register the callback
        self.mqtt_client.on_connect = self.myOnConnect

    def start(self):
        #manage connection to broker
        self.mqtt_client.connect('iot.eclipse.org', 1883)
        self.mqtt_client.loop_start()

    def stop(self):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()

    def myPublish(self, topic, message):
        # publish a message with a certain topic
        self.mqtt_client.publish(topic, message, 0)

    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        print("Connected to message broker with result code: "+ str(rc))

import datetime
import paho.mqtt.client as mqtt
import pandas as pd
import numpy as np

temp = pd.read_csv("temphumi.csv", sep=';').iloc[:,-4]
humi = pd.read_csv("temphumi.csv", sep=';').iloc[:,-3]

if __name__ == "__main__":

    temp_pub = MyPublisher("TempPub")
    humi_pub = MyPublisher("HumiPub")
    temp_pub.start()
    humi_pub.start()

    for i in range(len(temp)):
        timenow = time.ctime()
        print("Publishing: " + str(temp.iloc[i]) + "," + str(humi.iloc[i]))
        temp_pub.myPublish("/Turin/1234/sensors/temperature", temp.iloc[i])
        time.sleep(30)
        humi_pub.myPublish("/Turin/1234/sensors/humidity", humi.iloc[i])
        time.sleep(30)

    temp_pub.stop()
    humi_pub.stop()
