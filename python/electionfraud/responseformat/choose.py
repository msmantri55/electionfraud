# -*- python -*-

import electionfraud.responseformat.abc as abc
import electionfraud.responseformat.exception as rfx

class ChooseExactly(abc.Abstract):
    """
    A response format that limits the voter to exactly a certain number
    of choices, without weighting or ranking.
    The response is expected to be a sequence type with no repetition.
    """
    def __init__(self, exactly):
        self.exactly = exactly

    def validate(self, responses, field):
        if len(responses) != self.exactly:
            raise rfx.WrongNumberOfChoices('must choose exactly %d choices' % (self.exactly))
        self.detect_duplicates(responses)
        self.validate_choices(responses, field)

class ChooseNoMoreThan(abc.Abstract):
    """
    A response format that limits the voter to no more than a certain
    number of choices, without weighting or ranking.
    The response is expected to be a sequence type.
    """
    def __init__(self, maximum):
        self.maximum = maximum

    def validate(self, responses, field):
        if not isinstance(responses, set):
            raise rfx.ResponseException(self.__class__ + 'expects a set')
        if len(responses) > self.maximum:
            raise rfx.WrongNumberOfChoices('limited to no more than %d choices' % (self.maximum))
        self.detect_duplicates(responses)
        self.validate_choices(responses, field)
