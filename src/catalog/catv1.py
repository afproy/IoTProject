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
        for actor in myactor_list:
            print actor
       
        print "new actor data -> %s" %new_actor
        if new_actor["type"] == "device":
            print "NEW DEVICE"
        elif new_actor["type"] == "service":
            print "NEW SERVICE"
        elif new_actor["type"] == "interface":
            print "NEW INTERFACE"




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
        new_data = json.loads(body_payload)

   
        catalog = 'test.json'
        old_catalog = open(catalog, 'r').read()
        old_catalog_dict = json.loads(old_catalog)

        if not uri:
            # reads the BODY content of the POST Method
            body_payload = cherrypy.request.body.read()
            print "body_payload = %s" %body_payload
      


        elif uri[0] == "iamalive":
            
            #now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           
            actor_list = old_catalog_dict['actor']
            #print actor_list
            print "======================================"
            Catalog_checker().check_actor(actor_list, new_data)
            






            




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
