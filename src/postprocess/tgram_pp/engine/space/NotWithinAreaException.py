class NotWithinAreaException(Exception):
    """ Exception class NotWithinAreaException:

    Exception to be raised when a point (User) is not situated within the
    limits of a settlement when it should be the case.

    Attributes:
        msg (str): providing a more explicit explanation
    """

    def __init__(self, msg = "No longer within the area!"):
        """ Constructor of NotWithinAreaException;
        
        Args:
            (str): providing a more explicit explanation, has a value by
                default in case it is being raised without any message
        """
        super().__init__(msg)
        self.msg = msg