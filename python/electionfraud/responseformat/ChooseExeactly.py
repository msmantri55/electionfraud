# -*- python -*-

from electionfraud.responseformat import Abstract, ResponseException

class ChooseExactly(Abstract):

    """
    A response format that limits the voter to exactly a certain number
    of choices, without weighting or ranking.
    The response is expected to be a sequence type with no repetitio
    """

    def __init__(self, exactly):
        self.exactly = exactly

    def validate(self, responses, field):
        if len(responses) != self.exactly:
            raise ResponseException('must choose exactly %d choices' % (self.exactly))
        self.validate_choices(responses, field)
