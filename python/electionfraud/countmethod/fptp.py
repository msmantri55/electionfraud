# -*- python -*-

import collections

import electionfraud.countmethod.abc as efcmabc
import electionfraud.countmethod.exception as efcmx

class FirstPastThePost(efcmabc.AbstractCountMethod):
    """
    Your basic horse race.  The associated response format is most
    likely ChooseNoMoreThan(n) or ChooseExactly(n).  

    This is never a multi-round affair; if the results are not
    conclusive, then another election will be held with a reduced set
    of choices.  Protocols for reducing the set of choices are beyond
    the scope of this counting method.

    Results are stored as a collections.Counter object.

    The residue is simply the number of votes counted.
    """
    def __init__(self):
        self.residue = 0
        self.results = None
        self._counter = collections.Counter()
    
    def count(self, responses):
        for response in responses:
            self._counter.update(response)
        self.results = self._counter
        self.residue = sum(self._counter.values())

    def are_we_there_yet(self):
        if self.results is None:
            raise efcmx.IncompleteCount('nobody past the post yet')

    def interpret_result(self):
        self.are_we_there_yet()
        interpretation = ''
        for choice in self.results.keys():
            votes = self.results[choice]
            percentage = 100 * votes / self.residue
            interpretation += '%s got %d of %d votes (%.2f%%)\n' % (choice, votes, self.residue, percentage)
        return interpretation

    def interpret_residue(self):
        self.are_we_there_yet()
        return '%d total votes cast\n' % (self.residue)

    def leader(self):
        self.are_we_there_yet()
        first, _ = self._counter.most_common(1)[0]
        return first

    def trailer(self):
        self.are_we_there_yet()
        last, _ = self._counter.most_common()[-1]
        return last
