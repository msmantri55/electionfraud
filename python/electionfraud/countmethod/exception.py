# -*- python -*-

class CountException(Exception):
    """
    Raised when there is a problem with counting votes or interpreting
    the results of a count.
    """
    pass

class IncompleteCount(CountException):
    """
    Raised when the requested operation or information is not
    available because the count is not done yet.
    """
    pass
