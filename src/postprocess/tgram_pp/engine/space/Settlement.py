class Settlement:
    """ Class Settlement:
    
    Class representing a settlement of human beings, it is defined by the
    geographical coordinates of two points at two ends of the settlement.

    Attributes:
        nwLat (float): latitude of the North West point
        nwLong (float): longitude of the North West point
        seLat (float): latitude of the South East point
        seLong (float): longitude of the South East point
        deltaLat (float): latitude delta between the two points
        deltaLong (float): longitude deltat between the two points
    """

    def __init__(self, nwLat, nwLong, seLat, seLong):
        """ Constructor of Settlement:

        Initializes all its attributes, and calculates the deltas of latitude
        and longitude over which it is situated.

        Args:
            nwLat (float): latitude of the North West point
            nwLong (float): longitude of the North West point
            seLat (float): latitude of the South East point
            seLong (float): longitude of the South East point
        """
        self.nwLat  = nwLat
        self.nwLong = nwLong
        self.seLat  = seLat
        self.seLong = seLong
        self.deltaLat  = nwLat - seLat
        self.deltaLong = seLong - nwLong


    def isWithin(self, aLat, aLong):
        """ Method to know if a point is situated within a Settlement:

        Args:
            aLat (float): latitude of the point to test
            aLong (float): longitude of the point to test

        Returns
            True if the point is within the settlement, False otherwise
        """
        return (self.seLat <= aLat <= self.nwLat) and \
               (self.nwLong <= aLong <= self.seLong)
        