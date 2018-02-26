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
            payload_TH_status['unit'] = 'open/closed'
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


            self.rpi_pub.start()
            self.rpi_pub.mqtt_client.myPublish(self.topic, "payload_telegram")
            time.sleep(1)