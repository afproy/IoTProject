class User:
    """Class User:

    Class representing a User, a User is uniquely identified through his
    Telegram chat_ID.

    Attributes:
        chat_ID (int): unique identifier for a User
        latU (float): latitude of the user's position
        longU (float): longitude of the user's position
        bUmbrellaOpen (bool): status of its umbrella, True when open, False
            when closed
    """

    def __init__(self, chat_ID, latU, longU, bUmbrellaOpen):
        """ Constructor of User:

        Simply initializes its attributes.

        Attributes:
            chat_ID (int): unique identifier for a User
            latU (float): latitude of the user's position
            longU (float): longitude of the user's position
            bUmbrellaOpen (bool): status of its umbrella, True when open, False
                when closed
        """
        self.chat_ID       = chat_ID
        self.latU          = latU
        self.longU         = longU
        self.bUmbrellaOpen = bUmbrellaOpen


    def __hash__(self):
        return self.chat_ID


    def __eq__(self, other):
        return self.chat_ID == other.chat_ID


    def __str__(self):
        myself = "User " + str(self.chat_ID) + " in position (" \
                 + str(self.latU) + ", " + str(self.longU) + ")"
        return myself
