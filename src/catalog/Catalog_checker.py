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
            print "NEW DEVICE"
            
            if not any(device['deviceID'] == new_actor['deviceID'] for device in myactor_list['device']):
                print "Device not present -> register new Device"

                new_actor['last_update'] = now
                nr_of_devices = len(myactor_list['device'])
                print "there are now %s devices" %nr_of_devices
                
                print "************ device added to list"
                myactor_list['device'].append(new_actor)
                response_msg = "Registered new device with these data: %s " %json.dumps(new_actor, indent = 4)

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
                        response_msg = "Updated device with these data: %s " %json.dumps(new_actor, indent = 4)

                        print "===  myactor_list['device'][nr] before"
                        print myactor_list['device'][nr]
                        
                        myactor_list['device'][nr] = new_actor

                        print "===  myactor_list['device'][nr] after "
                        print myactor_list['device'][nr]

                        print "Updated myactor_list with %s" %new_actor
                    nr+=1


               

        elif new_actor["type"] == "service":
            print "NEW SERVICE"
        elif new_actor["type"] == "interface":
            print "NEW INTERFACE"
        
        return myactor_list, response_msg


        print "--------------------------------------------------------"
        print "-----------------  exits check_actor()  ----------------"
        print "--------------------------------------------------------"