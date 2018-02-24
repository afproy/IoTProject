import json
import requests
import time

'''
   This script is used to make POST requests to the catalog
   in ordet to test the device registration and update of 
   the information

   The original script is making post requests at every
   3 seconds with a different 'deviceID' -> in this way
   at every 3 seconds, the catalog will store a new device
   if it is not already existing. If it exists, the catalog 
       will remove it.
'''

url = 'http://0.0.0.0:8080/iamalive'
payload = {'type': 'device', 'deviceID': 111}
headers = {'content-type': 'application/json'}
i = 0
while True:
    i+=1
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print "request %s POST -> %s" %(i, payload)
    
    #payload['data'] = payload['data'] + 5
    payload['deviceID'] = payload['deviceID'] * 2

    time.sleep(3)