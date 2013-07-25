# -*- python -*-

import electionfraud.countmethod.abc as abc

class SingleTransferableVote(abc.AbstractCountMethod):
    """
    http://en.wikipedia.org/wiki/Single_Transferable_Vote
    http://en.wikipedia.org/wiki/Counting_Single_Transferable_Votes

    Redistributes surplus votes downward from the top-ranked candidate
    to lower-ranked candidates, and up from eliminated candidates,
    until the race has as many winners as necessary.

    In a race with N choices and V valid votes cast, the winning vote
    quota (Droop quota) is 1 + (V / (N + 1)), rounded up to the next
    integer if necessary.
    """

    def __init__(self):
        raise NotImplemented()

    def count(self, responses):
        raise NotImplemented()

