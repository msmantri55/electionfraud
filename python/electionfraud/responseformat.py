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

class InvalidChoice(ResponseException):
    """
    Raised when the voter makes a choice that was not in the set of
    acceptable choices.
    """
    pass

class DuplicateChoice(ResponseException):
    """
    Raised when the voter chooses something more than the rules permit.
    """
    pass

class NonIntegerRating(ResponseException):
    """
    Raised when the voter provides something other than an integer 
    in their rating of a choice.
    """
    pass

class NegativeRating(ResponseException):
    """
    Raised when the voter provides a negative integer in their rating
    of a choice.
    """
    pass

class OverMaximumRating(ResponseException):
    """
    Raised when the voter chooses a number beyond the permitted maximum
    in their rating of a choice.
    """
    pass

class OverBudget(ResponseException):
    """
    Raised when the voter exceeds their budget (sum of all ratings across 
    all choices).
    """
    pass

class SelfPair(ResponseException):
    """
    Raised when the voter attempts to pairwise rank a choice against itself.
    """
    pass

class MakeUpYourMind(ResponseException):
    """
    Raised when the voter attempts to pairwise rank two choices both ways.
    """
    pass

class Abstract:
    """
    The various response formats are derived from this abstract base class.
    """

    def validate(self, responses, field=None):
        """
        Checks that the response is in the right format (i.e. data type).
        May also do other checks at the response format's discretion.
        Must throw an exception if the response is not proper.
        Must return None if the response is proper.
        """
        raise ElectionException('responseformat not properly subclassed')
    
    def validate_choices(self, responses, field=None):
        """
        Validate a particular choice against the field.  
        Must return None if the choices all validate.
        Must throw an exception if a choice is not valid.
        When field = None, write-in choices are permitted.
        This simpler version should work for iterable responses.
        field can be any type that supports 'in' or 'not in' comparison.
        """
        if field is None:
            return
        for choice in responses:
            if choice not in field:
                raise InvalidChoice(choice, field)

    def detect_duplicates(self, responses):
        """
        Check the set of responses for duplicates, if necessary.
        Must return None if there are no duplicates.
        Must throw an exception if there are duplicates.
        This implementation compares the size of the original responses to 
        the size of a set()ed version.
        """
        if len(responses) > len(set(responses)):
            raise DuplicateChoice('duplicate choices not allowed')

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
            raise WrongNumberOfChoices('limited to no more than %d choices' % (self.maximum))
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
            raise WrongNumberOfChoices('all choices in field must be ranked')
        RankInOrderOfPreference.validate(self, responses, field)

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
            raise WrongNumberOfChoices('rank no more than %d choices' % (self.maximum))
        RankInOrderOfPreference.validate(self, responses, field)

class Ratings(Abstract):
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
                raise NonIntegerRating('ratings must be integers')
            if rating < 0:
                raise NegativeRating('ratings must not be negative')
            if rating > self.maximum:
                raise OverMaximumRating('ratings must not exceed %d' % (self.maximum))
        self.validate_choices(responses, field)
        self.detect_duplicates(responses)

    def validate_choices(responses, field):
        altresponses = [ choice for choice, rating in responses ]
        Abstract.validate_choices(altresponses, field)

    def detect_duplicates(responses):
        altresponses = [ choice for choice, rating in responses ]
        Abstract.detect_duplicates(altresponses)

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
        if sum([cost for choice, cost in responses]) > self.budget:
            raise OverBudget('exceeded budget of %d' % (self.budget))
        Ratings.validate(self, responses, field)

class Pairwise(Abstract):
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
                raise SelfPair('a choice must not be paired with itself')
        self.validate_choices(responses, field)
        self.detect_duplicates(responses)

    def validate_choices(self, responses, field):
        for response in responses:
            x, y = response
            if x not in field or y not in field:
                raise InvalidChoice(choice, field)
                
    def detect_duplicates(self, responses):
        for response in responses:
            if response in self._tally:
                raise DuplicateChoice('already seen this response')
            x, y = response
            esnopser = (y, x)
            if esnopser in self._tally:
                raise MakeUpYourMind('already seen the reverse of this response')
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
            raise WrongNumberOfChoices('must rank every pairwise possibility')
        Pairwise.validate(self, responses, field)
