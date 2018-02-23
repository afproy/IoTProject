#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 17:24:29 2018

@author: Johanna
"""

from MySubscriber import MySubscriber

import time
import json

if __name__ == "__main__":
    test = MySubscriber("Client1")
    test.start()
    a = 0
    print(test.clientID)
    #%%
    while (True):
        a=a+1
        test.mqtt_client.myPublish("/Turin/sensors/", json.dumps({"value": a, "unit": "u", 
                                                                  "timestamp": "ts"}))
        time.sleep(5)
		    
    test.stop()