#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 13:30:18 2018

@author: Johanna
"""
import time as t
import json

class Humidity:
    def __init__(self):
        self.firstMessage=None
        self.clock_old=None
        self.clock_new=None
        self.temp_hour=None
        self.temp_day=None
        self.count=0
        
        
    
    def calc(self,value,unit):
        if self.firstMessage==None:
            self.firstMessage=1
            self.clock_old=t.time
        
            
            #du lässt timer loslaufen und immer, wenn stunde wechselt prüfst du ob es einen average 
            #gab und schickst ihn. Sonst schickst du eine leere msg
            #genau das gleiche für tag
            #nächstes ziel ist aber erstmal eine kleine, einfache version zum laufen zu bringen
        
    def toMessage(self,city):
        self.count+=4
        topic="/%s/freeboard/temperature/hour" %city
        msg={"x-axis":{
                "title":{"text":"Hours"},
                "type": "datetime",
                "floor":0},
            "y-axis":{
                "title":{"text":"°C"},
                "minorTickInterval": "auto",
                "floor":0},
            "value":self.count
            }
        
        return True, topic, json.dumps(msg)