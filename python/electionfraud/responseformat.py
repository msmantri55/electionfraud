# -*- python -*-

from electionfraud.fraud import ElectionException

class ResponseException(ElectionException):
    """
    Raised when the voter's response doesn't match what the response 
    format requires.
    """
    pass

class WrongNumberOfChoices(ResponseException):
    """
    Raised when the voter was asked to make a certain number of choices,
    but didn't comply.
    """
    pass

class Abstract:
    """
    The various response formats are derived from this abstract base class.
    """

    def validate(self, responses, field=None):
        """
        Checks that the response is in the right format (i.e. data type)
        and that the choices in it are limited to the field of possible
        choices.  When field = None, write-in choices are permitted.
        If the data types match up properly, should then go on to 
        invoke:
        validate_choices
        detect_duplicates
        """
        raise ElectionException('responseformat not properly subclassed')
    
    def validate_choices(self, responses, field=None):
        """
        Validate a particular choice against the field.  When field = None,
        write-in choices are permitted.
        field can be any type that supports 'in' or 'not in' comparison.
        """
        if field == None:
            return
        for choice in responses:
            if choice not in field:
                raise InvalidChoiceException(choice, field)

    def detect_duplicates(self, responses):
        """
        Should work for the simpler derived classes.  Compares the size
        of the original responses to a mashed-into-set version.
        """
        if len(responses) > len(set(responses)):
            raise ResponseException('duplicate choices not allowed')

class ChooseExactly(Abstract):
    """
    A response format that limits the voter to exactly a certain number
    of choices, without weighting or ranking.
    The response is expected to be a sequence type with no repetition.
    """
    def __init__(self, exactly):
        self.exactly = exactly

    def validate(self, responses, field):
        if len(responses) != self.exactly:
            raise WrongNumberOfChoices('must choose exactly %d choices' % (self.exactly))
        self.detect_duplicates(responses)
        self.validate_choices(responses, field)

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

class RankInOrderOfPreference(Abstract):
    """
    A response format that requires the user to rank their choices in 
    order of preference, without weighting.
    The response is expected to be a list of choices, with the more
    preferred choices towards the front of the list.
    """
    def validate(self, responses, field):
        if not isinstance(responses.__class__, list):
            raise ResponseException(self.__class__ + 'wants a list')
        self.detect_duplicates(responses)
        self.validate_choices(responses, field)

class RankAllInOrderOfPreference(RankInOrderOfPreference):
    """
    A response format that requires the user to rank their choices in 
    order of preference, without weighting.  All of the choices must 
    in the field must be ranked.
    The response is expected to be a list of choices, with the more
    preferred choices towards the front of the list.
    """
    def validate(self, responses, field):
        if len(responses) != len(field):
            raise ResponseException('all choices in field must be ranked')
        RankInOrderOfPreference.validate(self, responses, field)
