# -*- python -*-

from electionfraud import ElectionException

class InvalidChoiceException(ElectionException):
    """
    """

    def __init__(self, choice, field):
        if field == None:
            raise ElectionException("write-in candidates were permitted")
        self.choice = choice
        self.field = field
