
"""
Created on Tue Feb 20 13:29:38 2018

@author: Johanna
"""
import numpy as np
from datetime import datetime
import json

class Temperature:
    
    def __init__(self):
        self.firstMessage=False
        self.hour_old=None
        self.hour_new=None
        self.day_old=None
        self.day_new=None
        self.temp_hour=None
        self.temp_day=np.zeros(24)
        self.unit=None
        self.sendHour=False
        self.sendDay=False
        
        
    
    def calc(self,value,unit):
        if not(self.firstMessage):
            self.firstMessage=True
            self.hour_old=datetime.now().minute
            self.day_old=datetime.now().day
            self.temp_hour=value
            self.unit=unit
        else:
            self.hour_new=datetime.now().minute
            self.day_new=datetime.now().day
            self.temp_hour=(self.temp_hour+value)/2
            if self.hour_new > self.hour_old:
                self.sendHour=True
            if self.day_new > self.day_old:
                self.sendDay=True
                
                
        
            
            #du lässt timer loslaufen und immer, wenn stunde wechselt prüfst du ob es einen average 
            #gab und schickst ihn. Sonst schickst du eine leere msg
            #genau das gleiche für tag
            #nächstes ziel ist aber erstmal eine kleine, einfache version zum laufen zu bringen
        
    def toMessageHour(self,city):
        topic=""
        msg=""
        flag=False
        if self.sendHour:
            topic_hour="/Turin/freeboard/temperature/hour" 
            msg_hour={"x-axis":{
                    "title":{"text":"Hours"},
                    "type": "datetime",
                    "floor":0},
                "y-axis":{
                    "title":{"text":self.unit},
                    "minorTickInterval": "auto",
                    "floor":0},
                    "value":self.temp_hour
                    }
            topic=topic_hour
            msg=json.dumps(msg_hour)
            flag=True
            self.temp_day[self.hour_old]=self.temp_hour
            self.temp_hour=0 #Problem: what if temperature is 0 or below?
            
        return flag, topic, msg
        
    def toMessageDay(self,city):
        topic=""
        msg=""
        flag=False
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
            flag=True
            self.temp_day[:]=0
            self.sendDay=False

        return flag, topic, msg
        
    