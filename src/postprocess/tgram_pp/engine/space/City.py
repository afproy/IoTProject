from engine.space.Settlement import Settlement
from engine.space.Neighborhood import Neighborhood
from engine.space.NotWithinAreaException import NotWithinAreaException
from engine.users.User import User
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class City(Settlement):
    """ Class City:
    
    Class representing a city, it is defined by its name and the coordinates 
    of two points at two ends of the city (which defines a Settlement).
    It allows the creation of a grid of smaller cells which have two lists: the
    list of the users having their umbrella open and the list of the users
    having their umbrella closed. It's a convenient way to place the users on
    the map in these sort of neighborhoods.

    Attributes:
        name (str): name of the city
        n (int): square root of the wanted number of neighborhoods composing
            the city, put differently, the city will be n neighborhoods wide
            and n neighboroods long
        grid (:obj: `list` of :obj: `list` of :obj: `Neighborhood`): grid of n*n
            neighborhoods
        mapping (:obj: `dict` of :obj: `Neighborhood`): dictionnary keeping
            track of what Neighborhood the users are in
    """

    def __init__(self, name, nwLat, nwLong, seLat, seLong, n, threshold):
        """ Constructor of City:

        Initializes the attributes of the class.

        Args:
            name (str): name of the city
            nwLat (float): latitude of the North West point
            nwLong (float): longitude of the North West point
            seLat (float): latitude of the South East point
            seLong (float): longitude of the South East point
            n (int): square root of the wanted number of neighborhoods composing
                the city
            threshold (int): threshold of open umbrellas per neighborhood after
                which a rain warning is sent
        """
        logger.info("Initializing representation of the city of %s!" % (name))
        super().__init__(nwLat, nwLong, seLat, seLong)
        self.name = name
        self.n = n
        self.createGrid(threshold)
        self.mapping = dict()


    def createGrid(self, threshold):
        """ Method to create the grid of Neighborhoods:
        
        It creates a grid of n*n neighborhoods, the neighborhoods all have the
        same size which is the length of the axis divided by n.

        Args:
            threshold (int): threshold of open umbrellas per neighborhood after
                which a rain warning is sent
        """
        quantumLatN  = self.deltaLat / self.n
        quantumLongN = self.deltaLong / self.n 
        self.grid = [None] * self.n
        for i in range(self.n):
            nwLatN = self.nwLat - i * quantumLatN
            seLatN = nwLatN - quantumLatN
            self.grid[i] = [None] * self.n
            for j in range(self.n):
                nwLongN = self.nwLong + j * quantumLongN
                seLongN = nwLongN + quantumLongN
                self.grid[i][j] = Neighborhood(nwLatN, nwLongN, seLatN, \
                                               seLongN, threshold)
        logger.info("Created grid of Neighborhood over the city of %s." \
                    % (self.name))


    def updateUser(self, chat_ID, latU, longU, bUmbrellaOpen):
        """ Method that updates the position of the user:

        Adds and removes users from Neighborhoods based on their current
        position. Receives the list of users within a Neighborhood who need to
        receive a rain warning.

        Args:
            chat_ID (int): chat_ID of the user, it identifies her/him
            latU (float): latitude of the user
            longU (float): longitude of the user
            bUmbrellaOpen (bool): True when the umbrella is open

        Returns:
            usersToBeNotified, the set of users to be notified
        """

        logger.info("Updating position of user %i in the grid." % chat_ID)

        # Finding out neighborhood of our user
        try:
            newNeighborhood = self.findNeighborhood(chat_ID, latU, longU)
        except NotWithinAreaException as e:
            logger.exception(e.msg)
            return

        user = User(chat_ID, latU, longU, bUmbrellaOpen)
        if (user in self.mapping) and (self.mapping[user] != newNeighborhood):
            self.mapping[user].removeUser(user)
        self.mapping[user] = newNeighborhood
        usersToBeNotified = self.mapping[user].addUser(user)

        return usersToBeNotified


    def findNeighborhood(self, chat_ID, latU, longU):
        """ Method to find out Neighborhood where the user is currently in:

        Args:
            chat_ID (int): chat_ID of the user, it identifies her/him
            latU (float): latitude of the user
            longU (float): longitude of the user

        Returns:
            Neighborhood: the Neighborhood where the user, if the user is
                within the limits of the City it has to return a Neighborhood

        Raises:
            NotWithinAreaException: if the user is not in the city
        """
        if not self.isWithin(latU, longU):
            raise NotWithinAreaException("User %i not in the city!" % chat_ID)
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j].isWithin(latU, longU):
                    logger.info("Placing user %i in Neighborhood (%i, %i)." % \
                          (chat_ID, i, j))
                    return self.grid[i][j]


    def printGrid(self):
        """ Method to print the grid of Neighborhoods:

        Useful when debugging the grid
        """
        for i in range(self.n):
            row = ""
            for j in range(self.n):
                row += str(self.grid[i][j])
                row += " "
            print(row)
        