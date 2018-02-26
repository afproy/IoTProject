import threading
import time
from MyPublisher import MyPublisher
import rpi_connector

#from sensors import *


class PublishTH(threading.Thread):
    '''
        PublishTH will run in the background a MQTT publisher
    '''
    
    def __init__(self, host, port, topic, location, chatID):
        '''
           add doc
        '''

        threading.Thread.__init__(self)
        self.daemon = True
        #self.interval = interval
        #self.headers = {'content-type': 'application/json'}

        self.rpi_pub = MyPublisher('RPI_1')
        self.location = location
        self.chatID = chatID
        self.topic = topic

        self.start()
        


    def run(self):
        bFlagStart = False
        chatID = 111
        location = {}
        location['latitude'] = 33
        location['longitude'] = 2

        while True:
            
            #start publishing
        
            payload_telegram = {}
            payload_telegram['chatID'] = chatID
            payload_telegram['location'] = location
            payload_telegram['status'] = 1 # state of the button

            payload_TH_status = {}
            payload_TH_status['type'] = 'button'
            payload_TH_status['value'] = 'open' # reading temp from button

            payload_TH_temp = {}
            payload_TH_temp['unit'] = 'C'
            payload_TH_temp['type'] = 'temperature'
            payload_TH_temp['value'] = 20 # reading temp from sensor
        
            payload_TH_humi = {}
            payload_TH_humi['unit'] = '%'
            payload_TH_humi['type'] = 'temperature'
            payload_TH_humi['value'] = 5020 # reading humi from sensor


            print payload_telegram
            print payload_TH_temp
            print payload_TH_humi
            print payload_TH_status

            print "-------------------"
            print self.chatID
            print self.location
            print "-------------------"

            t = 15
            h = 30
            
            # simulating the reading of button 
            x = int(raw_input("what is the button state? \n"))
            time.sleep(1)
            if x == 1:
                print "publishing"
                self.rpi_pub.start()
                self.rpi_pub.mqtt_client.myPublish(self.topic, "payload_telegram")
            elif x == 0:
                print "waiting for button to be pressed"
                time.sleep(1)
            