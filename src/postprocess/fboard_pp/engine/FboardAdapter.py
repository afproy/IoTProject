
"""
Created on Tue Feb 20 10:25:18 2018

@author: Johanna
"""
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), \
                                            './../../../mqtt/')))
from OurMQTT import OurMQTT
from engine.tools.Temperature import Temperature
from engine.tools.Humidity import Humidity
from engine.tools.SensorRegistry import SensorRegistry
import json
#import string

class FboardAdapter:
   

    def __init__(self,city):
        self.myFboardMqttSub = OurMQTT("FboardSub", "iot.eclipse.org",
                                           1883, self)
        #self.myFboardMqttPub = OurMQTT("FboardPub", "iot.eclipse.org",
         #                              1883, self)
        self.temp=Temperature()
        self.hum=Humidity()
        self.sensorReg=SensorRegistry()
        self.city=city
        
    def process(self):
        print("Starting to receive data with %s and send processed data with "
              % (self.myFboardMqttSub.clientID))
        self.myFboardMqttSub.start()
        #self.myFboardMqttPub.start()
        
    def rest(self):
        print("Finishing data procesing and datafeed to Freeboard with %s "
              % (self.myFboardMqttSub.clientID))
        self.myFboardMqttSub.stop()
        #self.myFboardMqttPub.stop()
    
    def notify(self, bError, topic, msg):
        print("ok here")
        
        if bError:
            if topic == "connection":
                print("/!\ Connection error of CityManager's MQTT client: %s"
                      % (msg))
                print("Shutting down...")
                sys.exit()
        else:
            print("------------")
            print("Topic: %s" % (topic))
            print("Message: %s" % (msg))
            jsonMsg = json.loads(msg)
            t=topic.split('/')[3]
            if FboardAdapter.msgComplete(jsonMsg):
                if t == "temperature" :
                    value = jsonMsg["value"]
                    unit = jsonMsg["unit"]
                    time = jsonMsg["timestamp"]
                    self.temp.calculate(value,unit,time)
                elif t == "humidity":
                    value = jsonMsg["value"]
                    unit = jsonMsg["unit"]
                    time = jsonMsg["timestamp"]
                    self.hum.calculate(value,unit,time)
                elif t == "status":
                    status = jsonMsg["value"]
                    umID = topic.split('/',1)[2]
                    self.sensorReg.register(umID, status)

    
    def send(self):
        flag_th, topic_th, msg_th = self.temp.toMessageHour(self.city) 
                                                        
        if flag_th:
            self.myFboardMqttSub.myPublish(topic_th,msg_th,0)
       # else:
        #    print("Sorry, right now no new temperature data is available")
        
        flag_td, topic_td, msg_td = self.temp.toMessageDay(self.city) 
                                                        
        if flag_td:
            self.myFboardMqttSub.myPublish(topic_td,msg_td,0)
        #else:
         #   print("Sorry, right now no new temperature data is available")
        
        flag_hh,topic_hh,msg_hh = self.hum.toMessage(self.city)
        if flag_hh:
            self.myFboardMqttSub.myPublish(topic_hh,msg_hh,0)
        #else:
         #   print("Sorry, right now no new humidity data is available")
            
        flag_hd,topic_hd,msg_hd = self.hum.toMessage(self.city) #ACHTUNG anpassen!
        if flag_hd:
            self.myFboardMqttSub.myPublish(topic_hd,msg_hd,0)
        #else:
         #   print("Sorry, right now no new humidity data is available")
        
        topic_s,msg_s=self.sensorReg.getNumber(self.city)
        self.myFboardMqttSub.myPublish(topic_s,msg_s,0)
        #print something if you dont send a message
        
        
    def msgComplete(msg):
        """ method to check whether the message received is complete
        Args:
            msg (:obj: `dict` of :obj: `JSON`): json payload received
        """
        return ("value" in msg) and ("timestamp" in msg)


