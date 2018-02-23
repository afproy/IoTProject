
"""
Created on Thu Feb  8 17:06:46 2018

@author: Johanna
"""
from MyPublisher import MyPublisher

import time
import json

if __name__ == "__main__":
    test = MyPublisher("Publisher1")
    test.start()
    a = 0
    print(test.clientID)
    #%%
    while (True):
        test.mqtt_client.myPublish("/Turin/1234/sensors/temperature", json.dumps({"value": a, "unit": "u", "timestamp": "ts"}))
        a=a+1
        time.sleep(5)
		    
    test.stop()