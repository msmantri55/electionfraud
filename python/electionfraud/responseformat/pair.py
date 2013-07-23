# -*- python -*-

import electionfraud.responseformat.abc as abc
import electionfraud.responseformat.exception as rfx

class Pairwise(abc.Abstract):
    """
    A response format that states preferences in pairwise matchups.
    The response is expected to be a list of 2-tuples, with the higher
    preference as the first element.
    """
    def __init__(self):
        self._tally = set()

    def validate(self, responses, field):
        for response in responses:
            if not isinstance(response, tuple):
                raise TypeError('responses must be tuples')
            x, y = response
            if x == y:
                raise rfx.SelfPair('a choice must not be paired with itself')
        self.validate_choices(responses, field)
        self.detect_duplicates(responses)

    def validate_choices(self, responses, field):
        for response in responses:
            x, y = response
            if x not in field or y not in field:
                raise rfx.InvalidChoice(choice, field)
                
    def detect_duplicates(self, responses):
        for response in responses:
            if response in self._tally:
                raise rfx.DuplicateChoice('already seen this response')
            x, y = response
            esnopser = (y, x)
            if esnopser in self._tally:
                raise rfx.MakeUpYourMind('already seen the reverse of this response')
            self._tally.add(response)

class AllPossiblePairwise(Pairwise):
    """
    A response format that states preferences in pairwise matchups.
    All possible pairwise matchups must be mentioned.
    The response is expected to be a list of 2-tuples, with the higher
    preference as the first element.
    """
    def validate(self, responses, field):
        if len(responses) != sum(range(len(field))):
            raise rfx.WrongNumberOfChoices('must rank every pairwise possibility')
        super().validate(responses, field)
