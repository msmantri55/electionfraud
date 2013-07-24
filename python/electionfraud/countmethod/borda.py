# -*- python -*-

import abc
import collections

import electionfraud.countmethod.abc as cmabc
import electionfraud.countmethod.exception as cmx

class BordaBase(cmabc.AbstractCountMethod, metaclass=abc.ABCMeta):
    """
    http://en.wikipedia.org/wiki/Borda_count

    Most often used with RankInOrderOfPreference-type methods.  

    The highest-rated choice receives the most points, second-highest
    gets second-most, ..., lowest-rated gets least.

    Sum the points to find the results.
    """

    def __init__(self):
        super().__init__()

    def count(self, responses):
        counter = collections.Counter()
        for response in responses:
            counter.update(self.transform(response))
        self.residue = counter.values()
        self.result = counter

    def are_we_there_yet(self):
        if self.results is None:
            raise cmx.IncompleteCount()
        
    @abc.abstractmethod
    def transform(self, response):
        """
        Every Borda method must define a ballot transformation that
        turns a list of ranked choices into a dict of {choice: score}.
        """
        raise NotImplemented()

    def interpret_result(self):
        self.are_we_there_yet()
        interpretation = ''
        for choice in self.result.keys():
            points = self.result[choice]
            interpretation += '%s got %d points\n' % (choice, points)
        return interpretation

    def interpret_residue(self):
        self.are_we_there_yet()
        return '%d total votes cast\n' % (self.residue)

    def leader(self):
        self.are_we_there_yet()
        first, _ = self.result.most_common(1)[0]
        return first

    def trailer(self):
        self.are_we_there_yet()
        last, _ = self.result.most_common()[-1]
        return last


class TraditionalBorda(BordaBase):
    """
    In a field of N choices, the highest-ranked is awarded N-1 points,
    next highest-ranked N-2 points, ..., and lowest or unranked are
    awarded 0.
    """
    def __init__(self, fieldsize):
        """
        For this counting method we must know how many choices are in
        the field so we can properly assign points to the top rank.
        """
        super().__init__()
        self.fieldsize = fieldsize

    def transform(self, response):
        transformed = dict()
        points = self.fieldsize - 1
        for choice in response:
            transformed[choice] = points
            points -= 1
        return transformed
        

class NauruBorda(BordaBase):
    """
    Must be used with RankAllInOrderOfPreference.  Instead of integral
    numbers of points, the Nth-ranked choice is awarded 1/N points.
    """
    def transform(self, response):
        transformed = dict()
        denominator = 1
        for choice in response:
            transformed[choice] = 1/denominator
            denominator += 1
        return transformed

    def interpret_result(self):
        self.are_we_there_yet()
        interpretation = ''
        for choice in self.result.keys():
            points = self.result[choice]
            interpretation += '%s got %f points\n' % (choice, points)
        return interpretation


class KiribatiBorda(TraditionalBorda):
    """
    Must be used with RankExactlyInOrderOfPreference(N), where N
    is less than the size of the field of choices.  Unranked choices
    are awarded 0 points.  (Supposedly Kiribati sets N=4.)

    This implementation awards N points for the top-ranked choice on
    the ballot, and down from there in increments of 1.  As such it
    needs to know the size of the field.
    """
    def transform(self, response):
        transformed = dict()
        points = self.fieldsize
        for choice in response:
            transformed[choice] = points
            points -= 1
        return transformed


class ModifiedBorda(BordaBase):
    """
    Encourages voters to rank all choices by awarding points based on
    how many choices the voter ranked.  e.g. in a field of N choices,
    where the voter's choices are worth (N, N-1, ..., 2, 1) points, if
    the voter ranks only M<N of them, then the voter's choices are worth
    (M, M-1, ..., 2, 1) points.
    """
    def transform(self, response):
        transformed = dict()
        points = len(self.response)
        for choice in response:
            transformed[choice] = points
            points -= 1
        return transformed

