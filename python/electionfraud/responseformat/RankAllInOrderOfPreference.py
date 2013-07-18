# -*- python -*-

from electionfraud.responseformat import RankInOrderOfPreference, ResponseException

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
