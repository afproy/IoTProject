import paho.mqtt.client as PahoMQTT
import time


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
			# A new message is received
			print ("Topic:'" + msg.topic+"', QoS: '"+str(msg.qos)+"' Message: '"+str(msg.payload) + "'")



if __name__ == "__main__":
	temp_sub = MySubscriber("MySubscriber 1")
	humi_sub = MySubscriber("MySubscriber 2")

	temp_sub.start()
	humi_sub.start()
	while True:
	 pass


