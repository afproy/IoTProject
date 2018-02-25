import json
import time
import datetime



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

        print "--------------------------------------------------------"
        print "-----------------  enter check_actor()  ----------------"
        print "--------------------------------------------------------"
        
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
            print actor
       
        print "new actor data -> %s" %new_actor
        if new_actor["type"] == "device":
            print "NEW data from DEVICE"
            actor_type = 'device'
            
            # check for devices if are present or not in the catalog
            if not any(device['deviceID'] == new_actor['deviceID'] for device in myactor_list['device']):
                print "Device not present -> register new Device"

                new_actor['last_update'] = now
                nr_of_devices = len(myactor_list['device'])
                print "there are now %s devices" %nr_of_devices
                
                print "************ device added to list"
                myactor_list['device'].append(new_actor)
                msg = {}
                msg['status'] = 'registered'
                msg['data'] = new_actor
                response_msg = json.dumps(msg, indent = 4)
                print response_msg

                
                nr_of_devices = len(myactor_list['device'])
                print "there are now %s devices" %nr_of_devices

                print myactor_list['device']
 
            else:
                print "-> Device EXISTS -> update the Device"
                nr = 0
                for device in myactor_list['device']:
                    print "---> existing device data -> %s" %device

                    if device['deviceID'] == new_actor['deviceID']:
                        
                        new_actor['last_update'] = now
                        print "Updated device -> %s" %new_actor
                        msg = {}
                        msg['status'] = 'updated'
                        msg['data'] = new_actor
                        response_msg = json.dumps(msg, indent = 4)

                        print "===  myactor_list['device'][nr] before"
                        print myactor_list['device'][nr]
                        
                        myactor_list['device'][nr] = new_actor

                        print "===  myactor_list['device'][nr] after "
                        print myactor_list['device'][nr]

                        print "Updated myactor_list with %s" %new_actor
                    nr+=1

        elif new_actor["type"] == "service":
            print "NEW data from SERVICE"
            actor_type = 'service'
            
            # check for services if are present or not in the catalog
            if not any(service['serviceID'] == new_actor['serviceID'] for service in myactor_list['service']):
                print "Service not present -> register new Service"


                new_actor['last_update'] = now
                nr_of_services = len(myactor_list['service'])
                print "there are now %s services" %nr_of_services
                
                print "************ service added to list"
                myactor_list['service'].append(new_actor)
                msg = {}
                msg['status'] = 'registered'
                msg['data'] = new_actor
                response_msg = json.dumps(msg, indent = 4)
                print response_msg

                
                nr_of_services = len(myactor_list['service'])
                print "there are now %s services" %nr_of_services

                print myactor_list['service']

            else:
                print "-> Service EXISTS -> update the Service"

                nr = 0
                for service in myactor_list['service']:
                    print "---> existing service data -> %s" %service

                    if service['serviceID'] == new_actor['serviceID']:
                        
                        new_actor['last_update'] = now
                        print "Updated service -> %s" %new_actor
                        msg = {}
                        msg['status'] = 'updated'
                        msg['data'] = new_actor
                        response_msg = json.dumps(msg, indent = 4)

                        print "===  myactor_list['service'][nr] before"
                        print myactor_list['service'][nr]
                        
                        myactor_list['service'][nr] = new_actor

                        print "===  myactor_list['service'][nr] after "
                        print myactor_list['service'][nr]

                        print "Updated myactor_list with %s" %new_actor
                    nr+=1

        elif new_actor["type"] == "interface":
            print "NEW data from INTERFACE"
            actor_type = 'interface'
        
            # check for interfaces if are present or not in the catalog
            if not any(interface['interfaceID'] == new_actor['interfaceID'] for interface in myactor_list['interface']):
                print "Interface not present -> register new Interface"


                new_actor['last_update'] = now
                nr_of_interfaces = len(myactor_list['interface'])
                print "there are now %s interfaces" %nr_of_interfaces
                
                print "************ interface added to list"
                myactor_list['interface'].append(new_actor)
                msg = {}
                msg['status'] = 'registered'
                msg['data'] = new_actor
                response_msg = json.dumps(msg, indent = 4)
                print response_msg

                
                nr_of_interfaces = len(myactor_list['interface'])
                print "there are now %s interfaces" %nr_of_interfaces

                print myactor_list['interface']

            else:
                print "-> Interface EXISTS -> update the Interface"

                nr = 0
                for interface in myactor_list['interface']:
                    print "---> existing interface data -> %s" %interface

                    if interface['interfaceID'] == new_actor['interfaceID']:
                        
                        new_actor['last_update'] = now
                        print "Updated interface -> %s" %new_actor
                        msg = {}
                        msg['status'] = 'updated'
                        msg['data'] = new_actor
                        response_msg = json.dumps(msg, indent = 4)

                        print "===  myactor_list['interface'][nr] before"
                        print myactor_list['interface'][nr]
                        
                        myactor_list['interface'][nr] = new_actor

                        print "===  myactor_list['interface'][nr] after "
                        print myactor_list['interface'][nr]

                        print "Updated myactor_list with %s" %new_actor
                    nr+=1

        
        return myactor_list, response_msg


        print "--------------------------------------------------------"
        print "-----------------  exits check_actor()  ----------------"
        print("--------------------------------------------------------"











