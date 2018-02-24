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

    def check_actor(self, file, msg):
        local_file = open(file, r)





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
        if not uri:
            # reads the BODY content of the POST Method
            body_payload = cherrypy.request.body.read()
            
            # open the catalog.json file in writing mode
            catalog_file = open('catalog.json','w')

            # write in the catalog.json 
            catalog_file.write(json.dumps(json.loads(body_payload),indent=4))
            catalog_file.close()

        elif uri[0] == "init_catalog":
            # reads the BODY content of the POST Method
            body_payload=cherrypy.request.body.read()
            
            # open the catalog.json file in writing mode
            catalog_file=open('catalog.json','w')

            # write in the catalog.json 
            catalog_file.write(json.dumps(json.loads(body_payload),indent=4))
            catalog_file.close() 

        elif uri[0] == "keep_alive_test":
            # reads the BODY content of the POST Method
            body_payload=cherrypy.request.body.read()
            pythondict = json.loads(body_payload)

            
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pythondict['last_uptade'] = now
            print "time = %s" %now

            
            msg = ""
            msg = "this is the new request -> %s" %json.dumps(pythondict)
            print "this is the new request -> %s" %pythondict
 
            return msg


        elif uri[0] == "keep_alive":
            # reads the BODY content of the POST Method
            body_payload=cherrypy.request.body.read()
            pythondict = json.loads(body_payload)

            
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pythondict['last_uptade'] = now
            print "time = %s" %now

            catalog_file=open('catalog.json','w')

            # write in the catalog.json 
            catalog_file.write(json.dumps(pythondict))
            catalog_file.close()            
            
            msg = ""
            msg = "this is the new request -> %s" %json.dumps(pythondict)
            print "this is the new request -> %s" %pythondict
 
            return msg


        elif uri[0] == "keep_alive2":
            # reads the BODY content of the POST Method
            body_payload=cherrypy.request.body.read()
            new_data = json.loads(body_payload)
            print "body_payload = %s" %new_data

            
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #new_date['last_update'] = now
            #print "time = %s" %now

            old_data=open('catalog.json','r').read()
            print "old_data = %s" %old_data
            
            old_data = json.loads(old_data)
            print old_data['type']['device']
           
            device_list = old_data['type']['device']
            
            if not any(d['deviceID'] == new_data['deviceID'] for d in device_list):
                print "Device not present"    
            else:
                print "Device EXISTS"





            




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
