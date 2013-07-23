# -*- python -*-

import electionfraud.countmethod.abc as abc
import electionfraud.countmethod.exception as cmx

class BordaBase(abc.Abstract):
    """
    http://en.wikipedia.org/wiki/Borda_count

    Most often used with RankInOrderOfPreference-type methods.  

    The highest-rated choice receives the most points, second-highest
    gets second-most, ..., lowest-rated gets least.

    Sum the points to find the results.
    """
    pass

class TraditionalBorda(BordaBase):
    """
    In a field of N choices, the highest-ranked is awarded N
    points, and lowest or unranked are awarded 1 point.  (Alternately,
    N-1 for highest and 0 for lowest or unranked.)
    """
    pass

class NauruBorda(BordaBase):
    """
    Must be used with RankAllInOrderOfPreference.  Instead of integral
    numbers of points, the Nth-ranked choice is awarded 1/N points.
    """
    pass

class KiribatiBorda(BordaBase):
    """
    Must be used with RankExactlyThanInOrderOfPreference(N), where N
    is less than the size of the field of choices.  Unranked choices
    are awarded 0 points.  (Supposedly Kiribati sets N=4.)
    """
    pass

class ModifiedBorda(BordaBase):
    """
    Encourages voters to rank all choices by awarding points based on
    how many choices the voter ranked.  e.g. in a field of N choices,
    where the voter's choices are worth (N, N-1, ..., 2, 1) points, if
    the voter ranks only M<N of them, then the voter's choices are worth
    (M, M-1, ..., 2, 1) points.
    """
    pass
