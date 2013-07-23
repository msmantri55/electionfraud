# -*- python -*-

import logging
logging.basicConfig(level=logging.WARNING)

import electionfraud.countmethod.irv as irv

class ContingentVote(irv.InstantRunoffVoting):
    """
    http://en.wikipedia.org/wiki/Contingent_vote

    This counting method is used with RankNoMoreThanInOrderOfPreference(N),
    where N is small, e.g. 2 ("Supplementary Vote") or 3 (Sri Lanka).  If
    there is no winner after the first round of counting, the field is reduced
    to the top two candidates, and votes transferred accordingly.
    
    The residue from this counting method is a list of rounds, guaranteed
    to be no longer than 2.  Each round is an instance of FirstPastThePost.

    The result is simply the last round in the residue.
    """

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def requalify(self, response, leaders):
        """
        Returns a modified ballot that preserves only the leaders.
        """
        return [x for x in response if x in leaders]

    def count(self, responses):
        this_round, half = self.count_leaders(responses)
        self.logger.debug(this_round.results.most_common())
        self.residue.append(this_round.results)
        maybe_winner = this_round.leader()
        if this_round.results[maybe_winner] > half:
            self.results = self.residue[-1]
            return
        leaders = [x for x,y in this_round.results.most_common(2)]
        next_round = [self.requalify(x, leaders) for x in responses]
        self.count(next_round)
