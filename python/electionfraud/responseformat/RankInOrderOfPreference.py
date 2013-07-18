# -*- python -*-

from electionfraud.responseformat import Abstract, ResponseException

class RankInOrderOfPreference(Abstract):

    """
    A response format that requires the user to rank their choices in 
    order of preference, without weighting.
    The response is expected to be a list of choices, with the more
    preferred choices towards the front of the list.
    """

    def validate(self, responses, field):
        """
        """
        if not isinstance(responses.__class__, list):
            raise ResponseException(self.__class__ + 'wants a list')
        self.detect_duplicates(responses)
        self.validate_choices(responses, field)
