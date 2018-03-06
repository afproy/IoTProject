import paho.mqtt.client as PahoMQTT
import time
import requests
import sys, os
import json

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
        self.ts_fields = ts["fields"]
        self.ts_channel_id = ts["channel_id"]

    def start(self):
        self._paho_mqtt.connect(self.broker_host, self.broker_port)
        self._paho_mqtt.loop_start()

        self._paho_mqtt.subscribe(self.topics[0], 0)

    def stop(self):
        self._paho_mqtt.unsubscribe(self.topics)

        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()


    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        print ("Connected to message broker with result code: " + str(rc))

    def myOnMessageReceived(self, paho_mqtt, userdata, msg):
        print ("Topic:'" + msg.topic + "', QoS: '" + str(msg.qos) + \
               "' Message: '" + str(msg.payload) + "'\n")

        x = (msg.payload.decode("utf-8"))
        print ("\n\n")
        mydict = (json.loads(x))

        print mydict
        temp = float((mydict['temperature']['value']))

        humi = float((mydict['humidity']['value']))

        headers = {'content-type': 'application/json'}
        payload = {'api_key': self.ts_writeapikey, 'channel_id': self.ts_channel_id, self.ts_fields[0]: humi,
               self.ts_fields[1]: temp}

        print self.ts_url
        r = requests.post(self.ts_url, data=json.dumps(payload), headers=headers)
        print r.content


if __name__ == "__main__":
    # Loading configuration file
    conf = json.load(open("conf.json", "r"))

    # 1) Perform registration to catalog by creating dedicated thread
    registration(conf)

    # 2) Retrieve information regarding broker
    broker_host, broker_port = getBroker(conf)

    # 3) Ask for information about next actor
    ts = conf["thingspeak"]

    topics = conf["catalog"]["registration"]["expected_payload"] \
        ["requirements"]["topics"]

    ts_adaptor_sub = MySubscriber("ts_adaptor_subscriber", broker_host, \
                                  broker_port, topics, ts)

    ts_adaptor_sub.start()

    while True:
        time.sleep(1)


