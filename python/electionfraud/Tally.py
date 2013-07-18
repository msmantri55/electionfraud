#!/usr/bin/env python3

class Tally:
    """
    Basic frequency counter.
    Even though it is less convenient, results are stored as tuples, because
    election results are supposed to be immutable once the count is done.
    If you want to re-count, then re-count!
    """
    
    def __init__(self):
        self.results = {}

    def tally(self, votes):
        for vote in votes:
            try:
                _, n = self.results[vote]
                self.results[vote] = (vote, 1 + n)
            except KeyError:
                self.results[vote] = (vote, 1)
