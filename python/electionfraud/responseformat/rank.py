# -*- python -*-

import electionfraud.responseformat.abc as abc
import electionfraud.responseformat.exception as rfx

class RankInOrderOfPreference(abc.Abstract):
    """
    A response format that requires the user to rank their choices in 
    order of preference, without weighting.
    The response is expected to be a list of choices, with the more
    preferred choices towards the front of the list.
    """
    def __init__(self):
        pass

    def validate(self, responses, field):
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
            raise rfx.WrongNumberOfChoices('all choices in field must be ranked')
        super().validate(responses, field)

class RankNoMoreThanInOrderOfPreference(RankInOrderOfPreference):
    """
    A response format that requires the user to rank their choices in 
    order of preference, without weighting.  No more than a certain 
    number of choices in the field may be ranked.
    The response is expected to be a list of choices, with the more
    preferred choices towards the front of the list.
    """
    def __init__(self, maximum):
        self.maximum = maximum

    def validate(self, responses, field):
        if len(responses) > self.maximum:
            raise rfx.WrongNumberOfChoices('rank no more than %d choices' % (self.maximum))
        super().validate(responses, field)
