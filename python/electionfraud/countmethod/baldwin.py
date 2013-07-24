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
    """

class BaldwinTraditional(BaldwinBase):

    def __init__(self, fieldsize):
        super().__init__()
        self.fieldsize = fieldsize

class BaldwinModified(BaldwinBase):
    
    def __init__(self):
        super().__init__()

    pass
