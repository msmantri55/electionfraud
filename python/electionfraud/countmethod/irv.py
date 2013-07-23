# -*- python -*-

import logging
logging.basicConfig(level=logging.WARNING)

import electionfraud.countmethod.exception as efcmx
import electionfraud.countmethod.mrx as mrx

class InstantRunoffVoting(mrx.MultiRoundExhaustible):
    """
    http://en.wikipedia.org/wiki/Instant-runoff_voting 

    The algorithm (and its perils) are best described above, however
    here is a short summary for the lazy.  If on a given round no
    choice has more than half the votes, the choice that received the
    fewest votes is eliminated, and the ballots that listed the
    eliminated choice as their highest preference are recounted in the
    next round as if that eliminated choice were not available.  
    """

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def count(self, responses):
        this_round, half = self.count_leaders(responses)
        self.logger.debug(this_round.results.most_common())
        self.residue.append(this_round.results)
        maybe_winner = this_round.leader()
        if this_round.results[maybe_winner] > half:
            self.results = self.residue[-1]
            return
        loser = this_round.trailer()
        next_round = [self.disqualify(x, loser) for x in responses]
        self.count(next_round)
        
    def interpret_residue(self):
        self.are_we_there_yet()
        interpretation = ''
        ctr = 1
        for round in self.residue:
            interpretation += 'Round %d:\n' % (ctr)
            interpretation += round.interpret_results()
        return interpretation

    def leader(self):
        self.are_we_there_yet()

    def trailer(self):
        self.are_we_there_yet()
