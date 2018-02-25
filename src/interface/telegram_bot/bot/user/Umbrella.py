import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class Umbrella:
    """Class Umbrella:
    
    Represents the umbrella of a user of our platform.

    Attributes:
        id (int): umbrella's ID
        rPIURL (str): URL of the raspberry PI / umbrella of the user
    """


    def __init__(self, umbrella_ID, chat_ID):
        """ Constructor of Umbrella:

        Initializes the attributes of the Umbrella. It sends a request to
        catalog to know how to contact the umbrella and then it will send
        the umbrella a message to pair the chat_id to the umbrella.

        Args:
            umbrella_ID (int): umbrella's ID
            chat_ID (int): chat's ID
        """
        self.id = umbrella_ID
        self.rPIURL = None
        logger.info("Sending GET request to catalog to know how to " \
                    "contact the umbrella of ID: %s." % (self.id))
        logger.info("Sending POST request to the umbrella to pair "\
                    "umbrella_ID: %s to chat_ID: %s." % (self.id, chat_ID))
    

    def updateID(self, umbrella_ID, chat_ID):
        """ Method to update the umbrella's ID:

        Does so by sending a request catalog to know how to contact the new
        umbrella and then it will send the umbrella a message to pair the
        chat_id to the umbrella.
    
        Args:
            umbrella_ID (int): umbrella's ID
            chat_ID (int): chat's ID
        """
        self.id = umbrella_ID
        logger.info("Sending GET request to catalog to know how to " \
                    "contact the umbrella of ID: %s." % (self.id))
        logger.info("Sending POST request to the umbrella to update pairing "\
                    "of umbrella_ID: %s to chat_ID: %s." % (self.id, chat_ID))

    def sendLocation(self, location, chat_ID):
        """ Method to update user's location:

        Args:
            location (:obj: `telegram.Location`): user's location
            chat_ID (int): chat's ID
        """
        logger.info("Sending POST request to the umbrella to set/update " \
                    "location of user with chat_ID %s." % (chat_ID))
        