#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 13:30:40 2018

@author: Johanna
"""
import json

class SensorRegistry:
    
    def __init__(self):
        self.registry=0
    
    def register(self,umID, status):
        self.registry+=1
    
    def getNumber(self,city):
        topic="/%s/freeboard/umbrellas" %city
        msg={"umbrellas":self.registry}
        return topic, json.dumps(msg)