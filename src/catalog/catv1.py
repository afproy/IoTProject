import cherrypy
import json
import requests
import time
import datetime


class Catalog_manager():
    '''
        This Class manages the Catalog.
        It exposes a number of WebServices in order to:
        
        1) Retrieve the entire content of the Catalog
        2) Retrieve informaton about a speciffic resource
    '''


    def __init__(self, file):
        '''
            Constructor of Catalog_manager:

            This method initialiaze the attributes 'broker' and 'port' by oppening the catalog.json
            file and takes from it the information about the broker IP-address and the port.

            Arguments:
                file (file): the JSON file containing the content of the catalog 
        '''
        file_conf=open(file,'r')
        self.conf=json.load(file_conf)
        self.broker=self.conf['broker']
        self.port=self.conf['port']
        file_conf.close()

    def print_catalog_WS(self):
        '''
            This WebService returns the content of the "catalog.json" at the current time
            by printing its entire content
        '''
        msg=(
        '''
        Network Settings:
        Broker:   %s 
        Port:     %d
        ''' % (self.conf['broker'],self.conf['port']))
       
        msg = msg + 'Next Settings to be added:'
        return msg

    
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



class Catalog_config():
    exposed= True

    def GET(self,*uri,**params):
        if not uri:
            return open('catalog.json')
        if uri[0] == 'print_catalog':
            return Catalog_manager('catalog.json').print_catalog_WS()


    def POST(self,*uri,**params):
        '''
            The method is used to update the information in the catalog.json file
        '''
        # reads the BODY content of the POST Method
        body_payload = cherrypy.request.body.read()
        new_data_dict = json.loads(body_payload)

        catalog_name = 'test_device.json'
        old_catalog = open(catalog_name, 'r').read()
        old_catalog_dict = json.loads(old_catalog)


        if not uri:
            # reads the BODY content of the POST Method
            body_payload = cherrypy.request.body.read()
            print "body_payload = %s" %body_payload
      


        elif uri[0] == "iamalive":
            
            #now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           
            actor_dict = old_catalog_dict['actor']
            print "actor dict datatype:  %s" %type(actor_dict)
            print "new_data datatype: %s" %type(new_data_dict)
            print "======================================"
            updated_actors, message = Catalog_checker().check_actor(actor_dict, new_data_dict)

            old_catalog_dict['actor'] = updated_actors

            catalog_file = open(catalog_name,'w')
            catalog_file.write(json.dumps(old_catalog_dict, indent=4))
            catalog_file.close()

            
        return message
            






            




if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
        }
    }
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.server.socket_port = 8080
    cherrypy.tree.mount (Catalog_config(), '/', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
