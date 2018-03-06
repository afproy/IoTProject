import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),  './../mqtt/')))
from OurMQTT import OurMQTT


class MyPublisher():

    def __init__(self, clientID, broker, port):
        self.clientID = clientID
        self.broker = broker
        self.port = port
        #self.mqtt_client = OurMQTT(self.clientID, "iot.eclipse.org", 1883, self) 
        self.mqtt_client = OurMQTT(self.clientID, broker, port, self) 
        

    def start(self):
        print("Running %s" % (self.clientID))
        self.mqtt_client.start()


    def stop(self):
        print("Ending %s" % (self.clientID))
        self.mqtt_client.stop ()


    def notify(self, topic, msg):
        if bError:
            if topic == "connection":
                print("/!\ Connection error of %s's MQTT client: %s" \
                      % (self.clientID, msg))
                print("Shutting down...")
                sys.exit()
