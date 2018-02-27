import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './../mqtt/')))
from OurMQTT import OurMQTT
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './../catalog/')))
from util import *
#from MyPublisher import MyPublisher
#from sensors import *
import requests
from pubThread import *
import cherrypy
import json
import time



chatID = None
location = None



class PiServer():
    exposed = True


    def GET(self, *uri, **params):
        pass
        

    def POST(self, *uri, **params):
        #receive chatID and location from tgram (AlexP)
        body_payload = cherrypy.request.body.read()
        new_data_dict = json.loads(body_payload)
        global chatID
        global location

        if uri[0] == 'pair_chatID':
            
            print "chatID = %s" %chatID
            chatID = new_data_dict['chatID']
            print "chatID = %s" %chatID


        elif uri[0] == 'set_location':
            
            print "location = %s" %location
            location = new_data_dict['location']
            print "location = %s" %location 

        if ((chatID != None) and (location != None)):
            print "==========ready to start the thread=========="
            start_thread()


if __name__ == '__main__':

    file_conf=open('conf.json','r')
    rpi_conf=json.load(file_conf)

    # registration
    registration(rpi_conf)


    # 2) Retrieve information regarding broker
    #broker_host, broker_port = getBroker(file_conf)
    broker_host = 'localhost'
    broker_port = 1883
    
    # 3) Ask for information about next actor
    # next_actor_requirements = getNextActorRequirements(file_conf)

 

    next_actor_requirements = getNextActorRequirements(rpi_conf)

    print next_actor_requirements



 


    host = rpi_conf['catalog']['registration']['expected_payload']['requirements']['host']
    port = rpi_conf['catalog']['registration']['expected_payload']['requirements']['port']

    url = rpi_conf['catalog']['URL']

    file_conf.close()

    topics = ["/Turin/+/notifications", "/Turin/+/sensors/temperature", "/Turin/+/sensors/humidity"]
    
    
    
    
    #IamAlive(url, payload, refresh_rate)
    
    def start_thread():
        global chatID
        global location

        print "i will start the thread"
        print "chatID = %s" %chatID
        print "location = %s" %location
        
        PublishTH(broker_host, broker_port, topics, location, chatID )


    
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
        }
    }

    
    cherrypy.server.socket_host = host
    cherrypy.server.socket_port = port
    cherrypy.tree.mount (PiServer(), '/', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()



