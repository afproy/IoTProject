import logging
import requests
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), \
                                            './../../../../catalog/')))
from util import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class Umbrella:
    """Class Umbrella:
    
    Represents the umbrella of a user of our platform.

    Attributes:
        id (str): umbrella's ID
        rPIURL (str): URL of the raspberry PI associated to the umbrella
        rPIURI (:obj: `list` of str): URIs provided by said raspberry PI
    """

    headers = {'content-type': 'application/json'}

    def __init__(self, umbrella_ID, chat_ID):
        """ Constructor of Umbrella:

        Initializes the attributes of the Umbrella. It sends a request to
        catalog to know how to contact the umbrella and then it will send
        the umbrella a message to pair the chat_id to the umbrella.

        Args:
            umbrella_ID (str): umbrella's ID
            chat_ID (int): chat's ID
        """
        self.id = umbrella_ID
        self.pairChatID(chat_ID)
    

    def pairChatID(self, chat_ID):
        """ Method to pair chat_ID with umbrella_ID:

        By contacting catalog to know how to contact associated raspberry PI
        and then by contacting the raspberry PI to do the pairing.

        Args:
            chat_ID (int): represents the ID of the chat of a particular user
        """
        logger.info("Sending GET request to catalog to know how to " \
                    "contact the umbrella of ID: %s." % (self.id))

        # Loading configuration file
        conf = json.load(open("conf.json", "r"))

        conf["catalog"]["next_actor"]["params"][0]["ID"] = self.id

        next_actors = conf["catalog"]["next_actor"]["params"]
        req = getNextActorRequirements(conf)

        if (len(req) == len(next_actors)) and (next_actors[0]["ID"] in req):
            
            req = req[next_actors[0]["ID"]]

            if req["access"] == "REST" and len(req) == 4:
                self.rPIURL = "http://" + req["host"] + ":" + str(req["port"]) \
                          + "/"
                self.rPIURI = req["uri"]
            else:
                logger.error("Communication between RainBot and raspberry PI" \
                             "has changed. Assistance required!")
                return
        else:
            logger.error("Error while getting next_actor_requirements!")
            

        logger.info("Sending POST request to the umbrella to pair "\
                    "umbrella_ID: %s to chat_ID: %s." % (self.id, chat_ID))
        url = self.rPIURL + self.rPIURI[0]
        payload = {"chatID": chat_ID}
        r = requests.post(url, headers=Umbrella.headers, \
                          data=json.dumps(payload))


    def updateID(self, umbrella_ID, chat_ID):
        """ Method to update the umbrella's ID:

        Does so by sending a request catalog to know how to contact the new
        umbrella and then it will send the umbrella a message to pair the
        chat_id to the umbrella.
    
        Args:
            umbrella_ID (str): umbrella's ID
            chat_ID (int): chat's ID
        """
        self.id = umbrella_ID
        self.pairChatID(chat_ID)


    def sendLocation(self, location, chat_ID):
        """ Method to update user's location:

        Args:
            location (:obj: `telegram.Location`): user's location
            chat_ID (int): chat's ID
        """
        logger.info("Sending POST request to the umbrella to set/update " \
                    "location of user with chat_ID %s." % (chat_ID))
        url = self.rPIURL + self.rPIURI[1]
        payload = { "chatID": chat_ID, \
                    "location": { "latitude": location.latitude, \
                                  "longitude": location.longitude}}
        r = requests.post(url, headers=Umbrella.headers, \
                          data=json.dumps(payload))
        