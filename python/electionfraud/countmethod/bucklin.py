# -*- python -*-

import electionfraud.countmethod.fptp as fptp
import electionfraud.countmethod.irv as irv

class Bucklin(irv.InstantRunoffVoting):
    """
    http://en.wikipedia.org/wiki/Bucklin_voting

    Much like InstantRunoffVoting and its cousins, Bucklin's method
    expects the voters to use one of the Rank*InOrderOfPreference 
    response formats.

    Rather than eliminating candidates, this method expands the pool
    of votes to tally.  In the Nth round, the voter's top N
    preferences are all considered with equal weight.
    """
    
    def __init__(self):
        super().__init__()
        
    def count(self, responses):
        return self.count_bucklin(1, responses)

    def count_bucklin(self, rd, responses):
        this_round, half = self.bucklin_leaders(rd, responses)
        self.residue.append(this_round.results)
        maybe_winner = this_round.leader()
        if this_round.results[maybe_winner] > half:
            self.result = self.residue[-1]
            return
        self.count_bucklin(1 + rd, responses)
        
    def bucklin_leaders(self, rd, responses):
        non_exhausted_votes = [x for x in responses if len(x)]
        half = int(len(non_exhausted_votes) / 2)
        round_choices = [x[0:rd] for x in responses]
        counter = fptp.FirstPastThePost()
        counter.count(round_choices)
        return (counter, half)

