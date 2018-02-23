
"""
Created on Tue Feb 20 13:30:18 2018

@author: Johanna
"""
import numpy as np
from datetime import datetime
import json

class Humidity:
    
    def __init__(self):
        self.firstMessage=False
        self.hour_old=None
        self.hour_new=None
        self.day_old=None
        self.day_new=None
        self.hum_hour=None
        self.hum_day=np.zeros(24)
        self.unit=None
        self.sendHour=False
        self.sendDay=False
        self.flag=False
        
        
    
    def calc(self,value,unit):
        if not(self.firstMessage):
            self.firstMessage=True
            self.hour_old=datetime.now().hour
            self.day_old=datetime.now().day
            self.hum_hour=value #CHECK if typecast is necessary (to double)
            self.unit=unit
        else:
            self.hour_new=datetime.now().hour
            self.day_new=datetime.now().day
            self.hum_hour=(self.hum_hour+value)/2
            if self.hour_new != self.hour_old:
                self.sendHour=True
            if self.day_new != self.day_old:
                self.sendDay=True
                
                
        
            
            #du lässt timer loslaufen und immer, wenn stunde wechselt prüfst du ob es einen average 
            #gab und schickst ihn. Sonst schickst du eine leere msg
            #genau das gleiche für tag
            #nächstes ziel ist aber erstmal eine kleine, einfache version zum laufen zu bringen
        
    def toMessage(self,city):
        topic=""
        msg=""
        if self.sendHour:
            topic_hour="/%s/freeboard/humidity/hour" %city
            msg_hour={"x-axis":{
                    "title":{"text":"Hours"},
                    "type": "datetime",
                    "floor":0},
                "y-axis":{
                    "title":{"text":self.unit},
                    "minorTickInterval": "auto",
                    "floor":0},
                    "value":self.hum_hour
                    }
            topic=topic_hour
            msg=json.dumps(msg_hour)
            self.flag=True
            self.hum_day[self.hour_old]=self.hum_hour
            self.hum_hour=0 #Problem: what if temperature is 0 or below?
        if self.sendDay:
            topic_day="/%s/freeboard/temperature/day" %city
            msg_day={"x-axis":{
                    "title":{"text":"Days"},
                    "type": "datetime",
                    "floor":0},
                "y-axis":{
                    "title":{"text":self.unit},
                    "minorTickInterval": "auto",
                    "floor":0},
                    "value":self.temp_day
                    }
            topic=topic_day
            msg=json.dumps(msg_day)
            self.flag=True
            self.hum_day[:]=0
            self.sendDay=False
        if self.sendDay and self.sendHour:
            topic=[topic_hour,topic_day]
            msg=json.dumps([msg_hour,msg_day])
            self.flag=True
            self.hum_day[:]=0
            self.hum_hour=0 #Problem: what if temperature is 0 or below?
            self.sendHour=False
            self.sendDay=False
    
            
        
        return self.flag, topic, msg
        
    