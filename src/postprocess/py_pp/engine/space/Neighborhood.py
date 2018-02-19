from engine.space.Settlement import Settlement

class Neighborhood(Settlement):
    """ Class Neighborhood:

    Represents a neighborhood within the grid that composes the city. As City
    it inherits from Settlement to benefit from it attributes and methods.
    A Neighborhood keeps track of its users who have their umbrella open and
    the ones who have their umbrella closed. This way it knows who are the
    users who need to be notified when the number of open umbrellas exceeds a
    certain threshold.

    Attributes:
        usersWOpenUmbrellas (:obj: `set` of :obj: `User`): set of users who
            have their umbrella open
        usersWClosedUmbrellas (:obj: `set` of :obj: `User`): set of users who
            have their umbrella closed
        threshold (int): threshold of open umbrellas per neighborhood after
            which a rain warning is sent
    """

    def __init__(self, nwLat, nwLong, seLat, seLong, threshold = 5):
        """ Constructor of Neighborhood:

        Initializes its two sets of users and sets the threshold (which by
        default is 5).

        Args:
            nwLat (float): latitude of the North West point
            nwLong (float): longitude of the North West point
            seLat (float): latitude of the South East point
            seLong (float): longitude of the South East point
            threshold (int): threshold of open umbrellas per neighborhood after
                which a rain warning is sent
        """
        super().__init__(nwLat, nwLong, seLat, seLong)
        self.usersWOpenUmbrellas = set()
        self.usersWClosedUmbrellas = set()
        self.threshold = threshold


    def addUser(self, user):
        """ Method to add a User to the Neighborhood:

        Depending on whether the umbrella of the user is open or not, it will
        be removed from one set and added to the other (if he was not already
        there). Also in charge of detecting, if any, the list of users who need
        to receive a rain warning.

        Args:
            user (:obj: `User`): user to add to the Neighborhood

        Returns:
            None if no user needs to be warned, a set of users otherwise
        """
        if user.bUmbrellaOpen:
            self.usersWClosedUmbrellas.discard(user)
            if user not in self.usersWOpenUmbrellas:
                self.usersWOpenUmbrellas.add(user)
                if len(self.usersWOpenUmbrellas) == self.threshold:
                    print("Sending notification to all users with closed" \
                          " umbrellas here")
                    return self.usersWClosedUmbrellas
        else:
            self.usersWOpenUmbrellas.discard(user)
            if user not in self.usersWClosedUmbrellas:
                self.usersWClosedUmbrellas.add(user)
                if len(self.usersWOpenUmbrellas) >= self.threshold:
                    print("Sending notification to new user %s" % str(user))
                    return [user]

        return None


    def removeUser(self, user):
        """ Method to remove a User from a Neighborhood

        Args:
            user (:obj: `User`): User to be removed
        """
        if user.bUmbrellaOpen:
            self.usersWOpenUmbrellas.discard(user)
        else:
            self.usersWClosedUmbrellas.discard(user)

    
    def __hash__(self):
        return hash((self.nwLat, self.nwLong, self.seLat, self.seLong))


    def __eq__(self, other):
        if other == None or not isinstance(other, Neighborhood):
            return False
        return (self.nwLat, self.nwLong, self.seLat, self.seLong) == \
               (other.nwLat, other.nwLong, other.seLat, other.seLong)


    def __str__(self):
        representation = {"coordinates": {"nwLat": self.nwLat, \
                          "nwLong": self.nwLong, "seLat": self.seLat, \
                          "seLong": self.seLong}}
        return str(representation)
