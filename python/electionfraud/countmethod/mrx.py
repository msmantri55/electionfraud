# -*- python -*-

import electionfraud.countmethod.abc as efcmabc
import electionfraud.countmethod.exception as efcmx
import electionfraud.countmethod.fptp as fptp

class MultiRoundExhaustible(efcmabc.AbstractCountMethod):
    """
    A base class for implementing counting methods that could possibly
    span multiple rounds, with choices disqualified between rounds for
    insufficient/excessive first/last place votes.  A voter's vote is
    considered exhausted if all of its choices have been disqualified.
    If there is a tie for first/last place at the end of a given
    round, the tie is broken arbitrarily.
    """

    def __init__(self):
        """
        The tally of each round depends on a FirstPastThePost
        computation.  The results attribute is in fact an instance of
        FirstPastThePost.  The residue is a list of FirstPastThePost
        instances, with the last instance being identical to the
        results.
        """
        self.residue = []
        self.results = None

    def disqualify(self, response, loser):
        """
        Returns a modified ballot, with an eliminated choice removed.
        """
        return [choice for choice in response if choice != loser]

    def count(self, responses):
        raise NotImplemented(self.__name__ + '.count')

    def count_leaders(self, responses):
        """
        Tallies up the first choices of all non-exhausted ballots via
        FirstPastThePost and returns a 2-tuple containing the results
        and the minimum number of votes required to win.  It is up to
        the real counting method to use this information appropriately.
        """
        non_exhausted_votes = [x for x in responses if len(x)]
        half = int(len(non_exhausted_votes) / 2)
        first_choices = [[x[0]] for x in responses if len(x)]
        counter = fptp.FirstPastThePost()
        counter.count(first_choices)
        return (counter, half)

    def are_we_there_yet(self):
        if self.results is None:
            raise efcmx.IncompleteCount()

    def interpret_result(self):
        self.are_we_there_yet()
        return 'Final round:\n' + self.results.interpret_result()

    def leader(self):
        self.are_we_there_yet()
        return self.results.leader()

    def trailer(self):
        self.are_we_there_yet()
        return self.results.trailer()
