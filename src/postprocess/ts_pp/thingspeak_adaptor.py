import paho.mqtt.client as PahoMQTT
import time
import requests
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), \
                                            './../../catalog/')))
from util import *

class MySubscriber:
		def __init__(self, clientID, broker_host, broker_port, topics, ts):
			self.clientID = clientID

			self._paho_mqtt = PahoMQTT.Client(clientID, False) 

			self._paho_mqtt.on_connect = self.myOnConnect
			self._paho_mqtt.on_message = self.myOnMessageReceived

			self.broker_host = broker_host
			self.broker_port = broker_port
			self.topics = topics
			self.ts_url = ts["URL"]
			self.ts_writeapikey = ts["writeapikey"]
			self.ts_params = ts["params"]


		def start (self):

			self._paho_mqtt.connect(self.broker_host, self.broker_port)
			self._paho_mqtt.loop_start()

			self._paho_mqtt.subscribe([(self.topics[0], 2), \
									   (self.topics[1], 2)])

		def stop (self):
			self._paho_mqtt.unsubscribe(self.topics)
			self._paho_mqtt.loop_stop()
			self._paho_mqtt.disconnect()

		def myOnConnect (self, paho_mqtt, userdata, flags, rc):
			print ("Connected to message broker with result code: "+str(rc))

		def myOnMessageReceived (self, paho_mqtt , userdata, msg):

			print ("Topic:'" + msg.topic + "', QoS: '" + str(msg.qos) + \
				   "' Message: '"+str(msg.payload) + "'\n")
			#if the topic is Temperature it writes in field2
			str_temp = self.topics[0].split("/")
			str_humi = self.topics[1].split("/")

			topic = msg.topic.split("/")


			if topic[-1] == str_temp[-1]:

				params = {
					self.ts_params[0] : self.ts_writeapikey,
					self.ts_params[2] : float(msg.payload)
				}

			elif topic[-1] == str_humi[-1]:

				params = {
					self.ts_params[0]: self.ts_writeapikey,
					self.ts_params[1]: float(msg.payload)
				}

			result = requests.get(self.ts_url, params=params)



if __name__ == "__main__":
	
	conf = json.load(open("conf.json", "r"))

	registration(conf)

	broker_host, broker_port = getBroker(conf)

	ts = conf["thingspeak"]

	topics = conf["catalog"]["registration"]["expected_payload"] \
				 ["requirements"]["topics"]

	ts_adaptor_sub = MySubscriber("ts_adaptor_subscriber", broker_host, \
								  broker_port, topics, ts)

	ts_adaptor_sub.start()

	while True:
		time.sleep(1)


