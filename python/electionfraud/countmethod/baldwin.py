# -*- python -*-

import abc

import electionfraud.countmethod.borda as borda
import electionfraud.countmethod.mrx as mrx

class BaldwinBase(mrx.MultiRoundExhaustible, metaclass=abc.ABCMeta):
    """
    http://en.wikipedia.org/wiki/Nanson%27s_method

    The multi-round mechanics of instant run-off, counted by a Borda
    method, last place eliminated each round, repeat until one
    candidate remains.

    Expected response format is Rank*InOrderOfPreference.

    Might be more willing to implement this if there were some easily
    accessible test data.  Also, the two sentences we have don't specify
    which variant of the Borda count to use...
    """
    def __init__(self):
        raise NotImplemented()

    def count(self, responses):
        raise NotImplemented()


class BaldwinTraditional(BaldwinBase):

    def __init__(self, fieldsize):
        super().__init__()
        self.fieldsize = fieldsize

class BaldwinModified(BaldwinBase):
    
    def __init__(self):
        super().__init__()

