# -*- python -*-

from collections import Counter

class FirstPastThePost(electionfraud.countmethod.Abstract):

    """
    A glorified frequency counter.
    """

    def __init__(self):
        self._counter = Counter()

    def count(self, response):
        self._counter.update(response)

    def results(self):
        return self._counter
