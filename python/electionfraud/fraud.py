# -*- python -*-

import uuid

class ElectionException(Exception):
    """
    Our own basic exception.  We expect it to be subclassed.
    """
    pass

class Choice:
    """
    Mostly a wrapper around strings to make them not act like sequence types.
    """

    namespace = 'urn:nog:dev:electionfraud:choice'

    def __init__(self, x):
        self._x = x
        self._u = uuid.uuid5(uuid.NAMESPACE_URL, Choice.namespace)
        
    def __str__(self):
        return str(self._x)

    def __repr__(self):
        return 'Choice:' + self._x
