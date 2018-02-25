import telegram
import logging

from bot.user.Umbrella import Umbrella

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class User(telegram.User):
    """Class User:

    Inherits from telegram.User and represents a Telegram user that uses our
    platform.

    Attributes:
        location (:obj: `telegram.Location`): location of our user
        umbrella (:obj: `Umbrella`): umbrella of our user
    """


    def __init__(self, usr, location = None, umbrella_ID = None):
        """ Constructor of User:

        Calls constructor of super class to initializes all its fields.
        Sets the location of the user and if we received the umbrella_ID of our
        user then we also instantiates her/his umbrella.

        Args:
            usr (:obj: `telegram.User`): Telegram user
            location (:obj: `telegram.Location`): location of our user
            umbrella_ID (int): identifiying user's umbrella_ID
        """
        super().__init__(usr.id, usr.first_name, usr.is_bot, usr.last_name,
                         usr.username, usr.language_code, usr.bot)
        self.location = location
        self.umbrella = None
        
        if umbrella_ID != None:
            self.umbrella = Umbrella(umbrella_ID, self.id)

        logger.info("Created user %s (ID: %s) in our system!" % (self.name, self.id))


    def setUmbrellaID(self, umbrella_ID):
        """ method to set the user's umbrella_ID
        Args:
            umbrella_ID (int): of the user's umbrella
        """
        self.umbrella = Umbrella(umbrella_ID, self.id)

    def updateUmbrellaID(self, umbrella_ID):
        """ method to update the user's umbrella_ID
        Args:
            umbrella_ID (int): of the user's umbrella
        """
        self.umbrella.updateID(umbrella_ID, self.id)

    def setLocation(self, location):
        """ method to set/update the user's location
        Args:
            location (:obj: `telegram.Location`): new location of the user
        """
        self.location = location
        if self.umbrella != None:
            self.umbrella.sendLocation(location, self.id)


    def __str__(self):
        me = "Name: %s / ID: %s / umbrella_ID: %s / Lat: %s - Long: %s"       \
             % (self.name, self.id, self.umbrella.id, self.location.latitude, \
                self.location.longitude)
        return me
