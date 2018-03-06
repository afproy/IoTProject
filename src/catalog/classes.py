import json
import time
import datetime
from threading import Thread
import requests

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class Catalog_checker():
    

    def check_actor(self, myactor_list, new_actor):
        '''
           This method checks the type of actor and register it, or updates if already registered
           
           Registering: -> creating a new field("last_update": "time") in the dictionary 'new_actor'
           and after ...TBC

           Updating: -> update the field "last_update" 

           ARGs:
              - myactor_list: (dict) - is a python dictionary with all the actors that are present
              in the catalog
              - new_actor: (dict) - is a python dictionary that contains the information received
              from the actor
        '''

        #print "--------------------------------------------------------"
        #print "-----------------  enter check_actor()  ----------------"
        #print "--------------------------------------------------------"
        
        '''
        print "myactor_list = %s" %myactor_list
        print "--------------------------------------------"
        print "myactor_list['device'] = %s" %myactor_list['device']
        print "--------------------------------------------"
        print "myactor_list['device'][0] = %s" %myactor_list['device'][0]
        print "--------------------------------------------"
        print "myactor_list['device'][0][deviceID] = %s" %myactor_list['device'][0]['deviceID']
        print "--------------------------------------------"
        '''
        
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for actor in myactor_list:
            print (actor)
       
        print ("new actor data -> %s" %new_actor)
        if new_actor["type"] == "device":
            print ("NEW data from DEVICE")
            actor_type = 'device'
            
            # check for devices if are present or not in the catalog
            if not any(device['deviceID'] == new_actor['deviceID'] for device in myactor_list['device']):
                print ("Device not present -> register new Device")

                new_actor['last_update'] = now
                nr_of_devices = len(myactor_list['device'])
                print ("there are now %s devices" %nr_of_devices)
                
                print ("************ device added to list")
                myactor_list['device'].append(new_actor)
                msg = {}
                msg['status'] = 'registered'
                msg['data'] = new_actor
                response_msg = json.dumps(msg, indent = 4)
                print (response_msg)

                
                nr_of_devices = len(myactor_list['device'])
                print ("there are now %s devices" %nr_of_devices)

                print (myactor_list['device'])
 
            else:
                print ("-> Device EXISTS -> update the Device")
                nr = 0
                for device in myactor_list['device']:
                    print ("---> existing device data -> %s" %device)

                    if device['deviceID'] == new_actor['deviceID']:
                        
                        new_actor['last_update'] = now
                        print ("Updated device -> %s" %new_actor)
                        msg = {}
                        msg['status'] = 'updated'
                        msg['data'] = new_actor
                        response_msg = json.dumps(msg, indent = 4)

                        print ("===  myactor_list['device'][nr] before")
                        print (myactor_list['device'][nr])
                        
                        myactor_list['device'][nr] = new_actor

                        print ("===  myactor_list['device'][nr] after ")
                        print (myactor_list['device'][nr])

                        print ("Updated myactor_list with %s" %new_actor)
                    nr+=1

        elif new_actor["type"] == "service":
            print ("NEW data from SERVICE")
            actor_type = 'service'
            
            # check for services if are present or not in the catalog
            if not any(service['serviceID'] == new_actor['serviceID'] for service in myactor_list['service']):
                print ("Service not present -> register new Service")


                new_actor['last_update'] = now
                nr_of_services = len(myactor_list['service'])
                print ("there are now %s services" %nr_of_services)
                
                print ("************ service added to list")
                myactor_list['service'].append(new_actor)
                msg = {}
                msg['status'] = 'registered'
                msg['data'] = new_actor
                response_msg = json.dumps(msg, indent = 4)
                print (response_msg)

                
                nr_of_services = len(myactor_list['service'])
                print ("there are now %s services" %nr_of_services)

                print (myactor_list['service'])

            else:
                print ("-> Service EXISTS -> update the Service")

                nr = 0
                for service in myactor_list['service']:
                    print ("---> existing service data -> %s" %service)

                    if service['serviceID'] == new_actor['serviceID']:
                        
                        new_actor['last_update'] = now
                        print ("Updated service -> %s" %new_actor)
                        msg = {}
                        msg['status'] = 'updated'
                        msg['data'] = new_actor
                        response_msg = json.dumps(msg, indent = 4)

                        print ("===  myactor_list['service'][nr] before")
                        print (myactor_list['service'][nr])
                        
                        myactor_list['service'][nr] = new_actor

                        print ("===  myactor_list['service'][nr] after ")
                        print (myactor_list['service'][nr])

                        print ("Updated myactor_list with %s" %new_actor)
                    nr+=1

        elif new_actor["type"] == "interface":
            print ("NEW data from INTERFACE")
            actor_type = 'interface'
        
            # check for interfaces if are present or not in the catalog
            if not any(interface['interfaceID'] == new_actor['interfaceID'] for interface in myactor_list['interface']):
                print ("Interface not present -> register new Interface")


                new_actor['last_update'] = now
                nr_of_interfaces = len(myactor_list['interface'])
                print ("there are now %s interfaces" %nr_of_interfaces)
                
                print ("************ interface added to list")
                myactor_list['interface'].append(new_actor)
                msg = {}
                msg['status'] = 'registered'
                msg['data'] = new_actor
                response_msg = json.dumps(msg, indent = 4)
                print (response_msg)

                
                nr_of_interfaces = len(myactor_list['interface'])
                print ("there are now %s interfaces" %nr_of_interfaces)

                print (myactor_list['interface'])

            else:
                print ("-> Interface EXISTS -> update the Interface")

                nr = 0
                for interface in myactor_list['interface']:
                    print ("---> existing interface data -> %s" %interface)

                    if interface['interfaceID'] == new_actor['interfaceID']:
                        
                        new_actor['last_update'] = now
                        print ("Updated interface -> %s" %new_actor)
                        msg = {}
                        msg['status'] = 'updated'
                        msg['data'] = new_actor
                        response_msg = json.dumps(msg, indent = 4)

                        print ("===  myactor_list['interface'][nr] before")
                        print (myactor_list['interface'][nr])
                        
                        myactor_list['interface'][nr] = new_actor

                        print ("===  myactor_list['interface'][nr] after ")
                        print (myactor_list['interface'][nr])

                        print ("Updated myactor_list with %s" %new_actor)
                    nr+=1    

        return myactor_list, response_msg

    '''
    # this function is used to test the removal of actors with
    # a POST request at http://0.0.0.0:8080/removeme
    
    def remove_old(self, myactor_list, time_to_live):
        #now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        now = time.time()
        remove_list = []

        for actor in myactor_list:
            #print actor
    
            for actor_type in myactor_list[actor]:
                #print actor_type
                actorID = actor+'ID'

                # retrieve string timestamp from 'last_update'
                old = actor_type['last_update']
                
                # convert string timestamp to python datetime object
                fmt = '%Y-%m-%d %H:%M:%S'
                d1 = datetime.datetime.strptime(old, fmt)  
                # print d1.timetuple()
                
                # convert datetime object to POSIX format 
                old_posix = time.mktime(d1.timetuple())
                
                # compute the difference in seconds
                difference_seconds = now - old_posix
                
                if difference_seconds > time_to_live:
                    print "actor removed"
                    remove_list.append(actor_type[actorID])

        #print "to remove -------------------"
        #print remove_list
        
        new_list = {}
        removed_actors = []
        for actor in myactor_list:
            actorID = actor+'ID'
            new_list[actor] = []
            for actor_type in myactor_list[actor]:
                if actor_type[actorID] not in remove_list:
                    # addition of actor in new list
                    new_list[actor].append(actor_type)
                else:
                    # list of removed actors
                    removed_actors.append(actor_type)
        
        #print new_list
        #print removed_actors
        
        return new_list, removed_actors
        '''

class Actor_removal(Thread):
    '''
        Thread class that will run in background and at a specific interval
        will remove actors that are older than a given time
    '''

    def __init__(self, catalog_name, time_to_live):
        '''
            for the initialization of the thread we need to provide the name
            if the catalog and a time_to_live for the actors
            if the difference between last update and curren time is bigger
            than time_to_live, the actor will be removed from catalog
        '''

        Thread.__init__(self)
        self.daemon = True
        self.time_to_live = time_to_live
        self.catalog_name = catalog_name
        self.start()


    def run(self):
        
        while True:
            print ('removing from "%s" at every %s seconds' %(self.catalog_name, self.time_to_live))
            
        
            old_catalog = open(self.catalog_name, 'r').read()
            old_catalog_dict = json.loads(old_catalog)
            myactor_list = old_catalog_dict['actor']

            now = time.time()
            remove_list = []

            for actor in myactor_list:
            #print actor
    
                for actor_type in myactor_list[actor]:
                    #print actor_type
                    actorID = actor+'ID'

                    # retrieve string timestamp from 'last_update'
                    old = actor_type['last_update']
                
                    # convert string timestamp to python datetime object
                    fmt = '%Y-%m-%d %H:%M:%S'
                    d1 = datetime.datetime.strptime(old, fmt)  
                    # print d1.timetuple()
                
                    # convert datetime object to POSIX format 
                    old_posix = time.mktime(d1.timetuple())
                
                    # compute the difference in seconds
                    difference_seconds = now - old_posix
                
                    if difference_seconds > self.time_to_live:
                        print ("actor removed")
                        remove_list.append(actor_type[actorID])

            #print "to remove -------------------"
            #print remove_list
        
            new_list = {}
            removed_actors = []
            for actor in myactor_list:
                actorID = actor+'ID'
                new_list[actor] = []
                for actor_type in myactor_list[actor]:
                    if actor_type[actorID] not in remove_list:
                        # addition of actor in new list
                        new_list[actor].append(actor_type)
                    else:
                        # list of removed actors
                        removed_actors.append(actor_type)

            print ("%s actors removed" %len(removed_actors))

            old_catalog_dict['actor'] = new_list
            catalog_file = open(self.catalog_name,'w')
            catalog_file.write(json.dumps(old_catalog_dict, indent=4))
            catalog_file.close()

            time.sleep(self.time_to_live)

class IamAlive(Thread):
    '''
        IamAlive class will run a thread to register and update the information
        of the actor to the catalog
    '''

    def __init__(self, url, payload, interval):
        '''
            Args:
               url - url at which the POST request should be sent
               payload - (dict) the payload to be converted into json and 
                         embedded into body of the POST method
               interval (int) - the time interval (seconds) to send the requests
        '''

        Thread.__init__(self)
        self.daemon = True
        self.url = url
        self.payload = payload
        self.interval = interval
        self.headers = {'content-type': 'application/json'}
        self.start()


    def run(self):
        
        while True:
            #print 'posting at: "%s" \n with the body: %s \n at each: %s seconds' \
            #%(self.url, self.payload, self.interval)

            r = requests.post(self.url, data=json.dumps(self.payload), headers=self.headers)

            logger.info("POST-> %s \n BODY: %s \n Interval: %s seconds" \
                        % (self.url, self.payload, self.interval))
    
            logger.info("Response from the catalog: %s" % r.content)

            time.sleep(self.interval)
     
