# -*- python -*-

from electionfraud import ElectionException

class ResponseException(ElectionException):

    """
    An exception that is raised when the voter's response doesn't match
    what the response format requires.
    """

    pass

