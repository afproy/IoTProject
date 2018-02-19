""" Serveur to run the html page of freeboard"""

import cherrypy


class Generator(object):
    exposed = True
    def GET (self, *uri, **params):
        return open("index.html")

if __name__ == '__main__':
    conf = {
    '/': {
    'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
    'tools.sessions.on': True,
    }

    }
    cherrypy.tree.mount (Generator(), '/', conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 9000})
    cherrypy.engine.start()
    cherrypy.engine.block()
