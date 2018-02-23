
"""
Created on Tue Feb 20 13:30:40 2018

@author: Johanna
"""
import json

class SensorRegistry:
    
    def __init__(self):
        self.registry=[]
        self.a=0
    
    def register(self,umID, status):
        if status and (not umID in self.registry) :
            self.registry.append(umID)
        elif (not status) and (umID in self.registry):
            self.registry.delete(umID)
    
    def getNumber(self,city):
        topic=""
        msg=""
        self.a+=1
        topic="/Turin/freeboard/umbrellas"
        msg={"umbrellas":self.a}#len(self.registry)}
        return topic, json.dumps(msg)