# -*- python -*-

from electionfraud.responseformat import Abstract, ResponseException

class ChooseNoMoreThan(Abstract):

    """
    A response format that limits the voter to no more than a certain
    number of choices, without weighting or ranking.
    The response is expected to be a sequence type.
    """

    def __init__(self, maximum):
        self.maximum = maximum

    def validate(self, responses, field):
        if not isinstance(responses, set):
            raise ResponseException(self.__class__ + 'expects a set')
        if len(responses) > self.maximum:
            raise ResponseException('limited to no more than %d choices' % (self.maximum))
        self.detect_duplicates(responses)
        self.validate_choices(responses, field)
