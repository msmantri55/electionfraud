# -*- python -*-

import abc

class AbstractCountMethod(metaclass=abc.ABCMeta):
    """
    Abstract base class for counting methods.  

    Must provide a public results attribute which is the final result
    of the computation.  The format is not prescribed here.

    Must provide a public residue attribute which can be used for
    inspecting the detailed results of the count, e.g. the progress in
    each round for run-offs or multi-round methods.  The format is not
    prescribed here.

    Idealy, it should be possible to computationally prove that the
    result is valid, given the residue.  At the very least, a human
    official familiar with the counting method should be able to
    justify the validity of the results in the context of the residue.
    """

    @abc.abstractmethod
    def __init__(self):
        self.results = None
        self.residue = None

    @abc.abstractmethod
    def count(self, ballots):
        """
        The basic entry point to actual vote counting.  Takes a bunch
        of ballots (iterable), which are limited to one question
        apiece, and filtered of all spoiled responses to the question.
        Since you don't know if you are just one polling place or
        the final aggregator of all polling places, ALL BALLOTS MUST
        BE COUNTED.  (Just because your precinct heavily favors X
        doesn't mean that X will win the election!)
        """
        raise NotImplemented()
    
    @abc.abstractmethod
    def interpret_result(self):
        """
        Returns a string which can be used to explain the results
        to a human.  The string should end with a newline.
        """
        raise NotImplemented()

    @abc.abstractmethod
    def interpret_residue(self):
        """
        Returns a string which can be used to explain the residue
        to a human.  The string should end with a newline.
        """
        raise NotImplemented()

    @abc.abstractmethod
    def leader(self):
        """
        Returns a list of choices which are considered to be leading, based
        on the results.
        """
        raise NotImplemented()

    @abc.abstractmethod
    def trailer(self):
        """
        Returns a list of choices which are considered to be in last place,
        based on the results.
        """
        raise NotImplemented()

    @abc.abstractmethod
    def are_we_there_yet(self):
        """
        Raises an exception if there are no results available.
        Returns without raising an exception otherwise.
        """
        raise NotImplemented()
