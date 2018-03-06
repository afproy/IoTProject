import threading
import time
from MyPublisher import MyPublisher

import string
import json
#from sensors import *


class PublishTH(threading.Thread):
    '''
        PublishTH will run in the background a MQTT publisher
    '''
    
    def __init__(self, broker, port, topics, location, chatID):
        '''
           add doc
        '''

        threading.Thread.__init__(self)
        self.daemon = True
        self.broker = broker
        self.port = port
        self.topics = topics
        self.rpi_pub = MyPublisher('RPI_1', broker, port)
        self.location = location
        self.chatID = chatID

        self.start()
        


    def run(self):
        bFlagStart = False
        telegram_topic = ""
        thingspeak_topic = ""
        for topic in self.topics:
            for item in topic:
                if item.find('notifications') != -1:
                    telegram_topic = string.replace(item, '+', str(self.chatID))
                
                if item.find('sensors') != -1:
                    item = string.replace(item, '+', str(self.chatID))
                    thingspeak_topic = string.replace(item, '#', 'thingspeak')


        print telegram_topic
        print thingspeak_topic
        self.rpi_pub.start()
        
        while True:
            
            payload_telegram = {}
            payload_telegram['chat_ID'] = self.chatID
            payload_telegram['location'] = {}
            payload_telegram['location']['latitude'] = self.location['latitude']
            payload_telegram['location']['longitude'] = self.location['longitude']

            
            # read the temperature and humidity, here it is simulated
            humidity, temperature = 10, 20
            #temperature, humidity = DHT11(17).read()

            payload_TH = {}
            payload_TH['temperature'] = {'value': temperature, 'unit':'C'}
            payload_TH['humidity'] = {'value': humidity, 'unit':'%'}
        

            print payload_telegram
            print payload_TH


            print "-------------------"
            print self.chatID
            print self.location
            print "-------------------"

            # simulating the reading of button 
            x = int(raw_input("what is the button state? \n"))
            # x = Button(21).read()
            time.sleep(0.1)
            
            if x == 1:
                print "Button pressed -> publish info to all actors"
                payload_telegram['status'] = "open" # state of the button
                print "publishing"
                time.sleep(1)
                self.rpi_pub.mqtt_client.myPublish(telegram_topic, json.dumps(payload_telegram))
                time.sleep(1)
                self.rpi_pub.mqtt_client.myPublish(thingspeak_topic, json.dumps(payload_TH))
          
            elif x == 0:
                print "Button NOT pressed -> publish status to telegram pp engine"
                print "publishing"
                print "waiting for button to be pressed and publish 'closed' status to telegram pp_engine"
                payload_telegram['status'] = "closed" # state of the button
                self.rpi_pub.mqtt_client.myPublish(telegram_topic, json.dumps(payload_telegram))
                time.sleep(1)
            