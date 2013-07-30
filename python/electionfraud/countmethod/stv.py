# -*- python -*-

import abc

import electionfraud.countmethod.abc as cmabc

class SingleTransferableVote(cmabc.AbstractCountMethod, metaclass=abc.ABCMeta):
    """
    http://en.wikipedia.org/wiki/Single_Transferable_Vote
    http://en.wikipedia.org/wiki/Counting_Single_Transferable_Votes

    Redistributes surplus votes downward from the top-ranked candidate
    to lower-ranked candidates, and up from eliminated candidates,
    until the race has as many winners as necessary.  Once a candidate
    has reached a certain quota they are considered to have won, and
    votes will no longer be distributed to them.

    Almost immediately we should see that the order in which the votes
    are counted affects the tally, as does how we choose which votes
    to redistribute.

    Methods for computing the quota are based on a formula involving
    the number of valid unspoiled votes (V), and the number of seats to
    be filled (N).  Such a method should degenerate reasonably when there is
    only one seat to be filled (i.e. the quota is V/2).

    There also exist several methods for choosing which votes to
    redistribute (Meek's, Warren's, Wright, Gregory).
    """

    def __init__(self, seats, redistributor):
        super().__init__()
        self.seats = seats
        self._redist = redistributor

    @abc.abstractmethod
    def quota(responses):
        """
        Given the number of valid unspoiled ballots, compute the quota
        for a choice to be considered elected by this method.
        """
        raise NotImplemented()

    def count(self, responses):
        raise NotImplemented()
