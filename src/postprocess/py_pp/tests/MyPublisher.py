import paho.mqtt.client as MQTT

class MyPublisher:
    def __init__(self, clientID):
        self.clientID = clientID

        # create an instance of paho.mqtt.client
        self.mqtt_client = MQTT.Client(self.clientID, False) 
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
        self.mqtt_client.publish(topic, message, 2)

    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        print("Connected to message broker with result code: " + str(rc))