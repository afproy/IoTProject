import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './../catalog/')))
from util import *

import cherrypy
import json
import time
from cherrypy.lib.static import serve_file



class FreeboardServer:
    @cherrypy.expose
    def index(self, name):
        return serve_file(os.path.join(static_dir, name))

if __name__=='__main__':
    static_dir = os.path.dirname(os.path.abspath(__file__))  # Root static dir is this file's directory.
    print "\nstatic_dir: %s\n" % static_dir

    file_conf=open('conf.json','r')
    freeboard_conf=json.load(file_conf)

    # registration
    registration(freeboard_conf)

    host = freeboard_conf['catalog']['registration']['expected_payload']['requirements']['host']
    port = freeboard_conf['catalog']['registration']['expected_payload']['requirements']['port']

    #host = '0.0.0.0'
    #port = 8001

    conf = {
        '/': {  # Root folder.
            'tools.staticdir.on':   True,  # Enable or disable this rule.
            'tools.staticdir.root': static_dir,
            'tools.staticdir.dir':  'freeboard',
        }
    }


    print (conf)

    cherrypy.server.socket_host = host
    cherrypy.server.socket_port = port

    cherrypy.tree.mount (FreeboardServer(), '/', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()


