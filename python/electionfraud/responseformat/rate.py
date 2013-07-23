# -*- python -*-

import electionfraud.responseformat.abc as abc
import electionfraud.responseformat.exception as rfx

class Ratings(abc.Abstract):
    """
    A response format that requires the user to rate each choice on an
    integer scale.
    The response is expected to be a list of (choice, integer) tuples,
    order irrelevant.
    """
    def __init__(self, maximum):
        self.maximum = maximum

    def validate(self, responses, field):
        for response in responses:
            _, rating = response
            if not isinstance(rating, int):
                raise rfx.NonIntegerRating('ratings must be integers')
            if rating < 0:
                raise rfx.NegativeRating('ratings must not be negative')
            if rating > self.maximum:
                raise rfx.OverMaximumRating('ratings must not exceed %d' % (self.maximum))
        self.validate_choices(responses, field)
        self.detect_duplicates(responses)

    def validate_choices(responses, field):
        altresponses = [ choice for choice, rating in responses ]
        super().validate_choices(altresponses, field)

    def detect_duplicates(responses):
        altresponses = [ choice for choice, rating in responses ]
        super().detect_duplicates(altresponses)

class Budget(Ratings):
    """
    A response format that grants the voter an integral number
    of votes, to distribute among the choices as they see fit.
    The response is expected to be a list of (choice, integer) tuples,
    order irrelevant.
    """
    def __init__(self, budget):
        self.budget = budget
        self.maximum = budget

    def validate(self, responses, field):
        spent = sum([cost for choice, cost in responses])
        if spent > self.budget:
            raise rfx.OverBudget('exceeded budget of %d' % (self.budget))
        super().validate(responses, field)
