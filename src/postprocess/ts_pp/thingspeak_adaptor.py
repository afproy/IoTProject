import paho.mqtt.client as PahoMQTT
import time
import requests

class MySubscriber:
		def __init__(self, clientID):
			self.clientID = clientID
			# create an instance of paho.mqtt.client
			self._paho_mqtt = PahoMQTT.Client(clientID, False) 

			# register the callback
			self._paho_mqtt.on_connect = self.myOnConnect
			self._paho_mqtt.on_message = self.myOnMessageReceived

			self.topic1 = 'temp/temp1'
			self.topic2 = 'humi/humi1'


		def start (self):
			#manage connection to broker
			self._paho_mqtt.connect('iot.eclipse.org', 1883)
			self._paho_mqtt.loop_start()
			# subscribe for a topic
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

			print ("Topic:'" + msg.topic+"', QoS: '"+str(msg.qos)+"' Message: '"+str(msg.payload) + "'\n")

			if msg.topic == self.topic1:

				writeapikey = 'TET7BW0DX9KFMYZP'
				url = 'https://api.thingspeak.com/update.json?'
				params = {
					"api_key" : writeapikey,
					"field2" : float(msg.payload)
				}

			elif msg.topic == self.topic2:

				writeapikey = 'TET7BW0DX9KFMYZP'
				url = 'https://api.thingspeak.com/update.json?'
				params = {
					"api_key": writeapikey,
					"field1": float(msg.payload)
				}

			result = requests.get(url, params)



if __name__ == "__main__":
	temp_sub = MySubscriber("MySubscriber 1")
	humi_sub = MySubscriber("MySubscriber 2")

	temp_sub.start()
	humi_sub.start()
	while True:
		time.sleep(1)


