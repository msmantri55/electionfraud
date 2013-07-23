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
