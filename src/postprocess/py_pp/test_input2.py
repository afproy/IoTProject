import paho.mqtt.client as MQTT
import time
import json


class MyPublisher:
    def __init__(self, clientID):
        self.clientID = clientID

        self.mqtt_client = MQTT.Client(self.clientID, True)
        self.mqtt_client.on_connect = self.myOnConnect

    def start(self):

        self.mqtt_client.connect('mqtt.thingspeak.org', 1883)
        self.mqtt_client.loop_start()

    def stop(self):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()

    def myPublish(self, topic, message):

        self.mqtt_client.publish(topic, message, 0)

    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        print("Connected to message broker with result code: "+ str(rc))

class MySubscriber:
	def __init__(self, clientID):
		self.clientID = clientID

		self._paho_mqtt = MQTT.Client(clientID, False)

		self._paho_mqtt.on_connect = self.myOnConnect
		self._paho_mqtt.on_message = self.myOnMessageReceived

		self.topic1 = 'temp/temp1'
		self.topic2 = 'humi/humi1'


	def start (self):

		self._paho_mqtt.connect('iot.eclipse.org', 1883)
		self._paho_mqtt.loop_start()
		self._paho_mqtt.subscribe(self.topic1, 2)
		self._paho_mqtt.subscribe(self.topic2, 2)

	def stop (self):
		self._paho_mqtt.unsubscribe(self.topic)
		self._paho_mqtt.loop_stop()
		self._paho_mqtt.disconnect()

	def myOnConnect (self, paho_mqtt, userdata, flags, rc):
		print ("Connected to message broker with result code: "+str(rc))
        pass

	def myOnMessageReceived (self, paho_mqtt , userdata, msg):
		print ("Topic:'" + msg.topic+"', QoS: '"+str(msg.qos)+"' Message: '"+str(msg.payload) + "'")


import datetime
import paho.mqtt.client as mqtt
import pandas as pd
import numpy as np


if __name__ == "__main__":

    temp_pub = MyPublisher("TempPub")
    humi_pub = MyPublisher("HumiPub")
    temp_sub = MySubscriber("MySubscriber 1")
    humi_sub = MySubscriber("MySubscriber 2")

    temp_sub.start()
    humi_sub.start()
    while True:


        temp_pub.start()
        humi_pub.start()


        timenow = time.ctime()
        print "Publishing: " + str(temp.iloc[i]) + "," + str(humi.iloc[i])
        temp_pub.myPublish("channels/426828/publish/fields/field2/TET7BW0DX9KFMYZP", self.topic1)
        time.sleep(30)
        humi_pub.myPublish("channels/426828/publish/fields/field2/TET7BW0DX9KFMYZP", self.topic2)
        time.sleep(30)

    temp_pub.stop()
    humi_pub.stop()
