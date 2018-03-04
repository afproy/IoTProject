import threading
import time
from MyPublisher import MyPublisher
#import rpi_connector
import string
import json
from sensors import *


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
        temperature_topic = ""
        humidity_topic = ""
        for topic in self.topics:
            if topic.find('notifications') != -1:
                topic = string.replace(topic, '+', str(self.chatID))
                telegram_topic = topic
            if topic.find('temperature') != -1:
                topic = string.replace(topic, '+', str(self.chatID))
                temperature_topic = topic
            if topic.find('humidity') != -1:
                topic = string.replace(topic, '+', str(self.chatID))
                humidity_topic = topic
        while True:
            
            payload_telegram = {}
            payload_telegram['chatID'] = self.chatID
            payload_telegram['location'] = {}
            payload_telegram['location']['latitude'] = self.location['latitude']
            payload_telegram['location']['longitude'] = self.location['longitude']


            #humidity, temperature = 10, 20
            temperature, humidity = DHT11(17).read()

            payload_TH_temp = {}
            payload_TH_temp['unit'] = 'C'
            payload_TH_temp['type'] = 'temperature'
            payload_TH_temp['value'] = temperature # reading temp from sensor
        
            payload_TH_humi = {}
            payload_TH_humi['unit'] = '%'
            payload_TH_humi['type'] = 'humidity'
            payload_TH_humi['value'] = humidity # reading humi from sensor


            print payload_telegram
            print payload_TH_temp
            print payload_TH_humi

            print "-------------------"
            print self.chatID
            print self.location
            print "-------------------"

            # simulating the reading of button 
            #x = int(raw_input("what is the button state? \n"))
            x = Button(21).read()
            
            time.sleep(1)
            if x == "open":
                print "button is pressed, publish info to all actors"
                payload_telegram['status'] = "open" # state of the button
                print "publishing"
                self.rpi_pub.start()
                time.sleep(0.1)
                self.rpi_pub.mqtt_client.myPublish(telegram_topic, json.dumps(payload_telegram))
                self.rpi_pub.mqtt_client.myPublish(temperature_topic, json.dumps(payload_TH_humi))
                self.rpi_pub.mqtt_client.myPublish(humidity_topic, json.dumps(payload_TH_temp))
            elif x == "closed":
                print "waiting for button to be pressed"
                payload_telegram['status'] = "closed" # state of the button
                self.rpi_pub.mqtt_client.myPublish(telegram_topic, json.dumps(payload_telegram))
                time.sleep(1)
            