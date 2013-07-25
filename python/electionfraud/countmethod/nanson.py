# -*- python -*-

class Nanson:
    """
    http://en.wikipedia.org/wiki/Nanson%27s_method

    A multi-round system that eliminates candidates based on doing
    poorly (below average) in the Borda count.

    Now if only someone would define what the average is.  Theoretical
    average in a field of N candidates, assuming random vote
    distribution?  Straight arithmetic mean of point totals after a
    count?  Something else?
    """

    def __init__(self):
        super().__init__()

    def count(self, responses):
        raise NotImplemented()
        
