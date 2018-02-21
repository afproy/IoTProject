#!/usr/bin/env python2
# -*- coding: utf-8 -*-
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

class FboardAdapter:
   

    def __init__(self,city):
        
        self.myFboardMqttSub = OurMQTT("FboardSub", "iot.eclipse.org",
                                           1883, self)
        self.myFboardMqttPub = OurMQTT("FboardPub", "iot.eclipse.org",
                                       1883,self)
        self.temp=Temperature()
        self.hum=Humidity()
        self.sensorReg=SensorRegistry()
        self.city=city
        
    def process(self):
        
        print("Starting to receive data with %s and send processed data with %s "
              % (self.myFboardMqttSub.clientID,self.myFboardMqttPub.clientID))
        self.myFboardMqttSub.start()
        self.myFboardMqttPub.start()
        
    def rest(self):
        
        print("Finishing data procesing and datafeed to Freeboard with %s and %s "
              % (self.myFboardMqttSub.clientID,self.myFboardMqttPub.clientID))
        self.myFboardMqttSub.stop()
        self.myFboardMqttPub.stop()
    
    def notify(self, bError, topic, msg):
        
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
            if FboardAdapter.msgComplete(jsonMsg):
                if topic == "/+/freeboard/+/+/temperature":
                    value = jsonMsg["value"]
                    unit = jsonMsg["unit"]
                    time = jsonMsg["timestamp"]
                    self.temp.calculate(value,unit,time)
                elif topic == "/+/freeboard/+/+/humidity":
                    value = jsonMsg["value"]
                    unit = jsonMsg["unit"]
                    time = jsonMsg["timestamp"]
                    self.hum.calculate(value,unit,time)
                elif topic == "/+/freeboard/+/+/status":
                    status = jsonMsg["value"]
                    umID = topic.split('/',1)[2]
                    self.sensorReg.register(umID, status)

    
    def send(self):
        flag_t, topic_t, msg_t = self.temp.toMessage(self.city) #ACHTUNG: wenn sowohl stunde als auch tag geteilt werden muss
                                                        # geht das als [,] Liste für topic und msg
        if flag_t:
            self.myFboardMqttPub.myPublish(topic_t,msg_t)
        
        flag_h,topic_h,msg_h = self.hum.toMessage(self.city)
        if flag_h:
            self.myFboardMqttPub.myPublish(topic_h,msg_h)
        
        topic_s,msg_s=self.sensorReg.getNumber(self.city)
        self.myFboardMqttPub.myPublish(topic_s,msg_s)
        
        
    def msgComplete(self,msg):
        """ method to check whether the message received is complete
        Args:
            msg (:obj: `dict` of :obj: `JSON`): json payload received
        """
        return ("value" in msg) and ("timestamp" in msg)


