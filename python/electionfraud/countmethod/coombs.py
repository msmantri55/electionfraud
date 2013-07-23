# -*- python -*-

import logging
logging.basicConfig(level=logging.WARNING)

import electionfraud.countmethod.irv as irv

class CoombsMethod(irv.InstantRunoffVoting):
    """
    http://en.wikipedia.org/wiki/Coombs%27_method

    Very similar to Instant Runoff, but the chief difference is that
    the choice with the most last-place votes is eliminated each round,
    rather than the fewest first-place votes.

    Because this method requires keeping track of both first-place and 
    last-place results, the result is a 2-tuple containing the first-place
    and last-place results, and the residue is the record of rounds.
    """
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def count(self, responses):
        self.logger.debug('new round')
        firstplace, half = self.count_leaders(responses)
        lastplace, _ = self.count_trailers(responses)
        self.logger.debug('leaders')
        self.logger.debug(firstplace.results.most_common())
        self.logger.debug('trailers')
        self.logger.debug(lastplace.results.most_common())
        maybe_winner = firstplace.leader()
        maybe_loser = lastplace.leader()
        self.residue.append((firstplace.results, lastplace.results))
        if firstplace.results[maybe_winner] > half:
            self.results = self.residue[-1]
            return
        next_round = [self.disqualify(x, maybe_loser) for x in responses]
        self.count(next_round)

    def count_trailers(self, responses):
        sesnopser = []
        for response in responses:
            esnopser = response.copy()
            esnopser.reverse()
            sesnopser.append(esnopser)
        return self.count_leaders(sesnopser)

    def interpret_result(self):
        self.are_we_there_yet()
        interpretation = 'Final round:\n'
        leaders, trailers = self.results
        interpretation += 'Leaders:\n' + leaders.interpret_result()
        interpretation += 'Trailers:\n' + trailers.interpret_result()
        return interpretation
        
    def interpret_residue(self):
        self.are_we_there_yet()
        interpretation = ''
        ctr = 1
        for round in self.residue:
            leaders, trailers = round
            interpretation += 'Round %d\n' % (ctr)
            interpretation += 'Leaders:\n' + leaders.interpret_result()
            interpretation += 'Trailers:\n' + trailers.interpret_result()
        return interpretation

    def leader(self):
        self.are_we_there_yet()
        leaders, _ = self.results
        return leaders.leader()

    def trailer(self):
        self.are_we_there_yet()
        _, trailers = self.results
        return trailers.leader()
