# -*- python -*-

import collections.abc
import fractions
import logging
import random

logging.basicConfig(level=logging.DEBUG)

class Redistributor(collections.abc.Iterable):
    """
    A method for choosing which votes to count first when
    redistributing votes downward in a single transferable vote.
    Instances of this class should behave properly under the iterator
    protocol.
    """
    def __init__(self, responses):
        self.responses = responses

    def __next__(self):
        return NotImplemented()

    def __call__(self):
        return NotImplemented()

    def __iter__(self):
        return NotImplemented()

class Identity(Redistributor):
    """
    Chooses all votes in their original order.  Not really much of a
    redistributor, is it?
    """
    def __next__(self):
        return iter(self.responses)

    __iter__ = __next__
    __call__ = __next__

class NthSubset(Redistributor):
    """
    Chooses every Nth ballot.  Raises ValueError if N and
    len(responses) are not relatively prime, because potentially every
    ballot could be counted.
    """
    def __init__(self, responses, n):
        if n == 1:
            raise ValueError('trivial redistribution not supported')
        if fractions.gcd(len(responses), n) != 1:
            raise ValueError('n and len(responses) must be relatively prime')
        self._nth = n
        self._current = None
        self._remaining = len(responses)
        self.logger = logging.getLogger(__name__)
        super().__init__(responses)

    def __next__(self):
        """
        """
        self.logger.debug('initial next()')
        self._current = -1
        try:
            while True:
                try:
                    self.logger.debug('previous remaining: %d', self._remaining)
                    self.logger.debug('previous current: %d', self._current)
                    if self._remaining:
                        self._current = (self._current + self._nth) % len(self.responses)
                        self._remaining -= 1
                        self.logger.debug('new current: %d', self._current)
                        self.logger.debug('new remaining: %d', self._remaining)
                        yield self.responses[self._current]
                    else:
                        raise StopIteration()
                finally:
                    pass
        finally:
            pass
        self.logger.debug('fell off the end')
        return None
                
    __call__ = __next__
    __iter__ = __next__

class Cincinnati(NthSubset):
    """
    A specialization of NthSubset, with N = 11.  Supposedly used in
    the city of Cambridge, Massachusetts.
    """
    def __init__(self, responses):
        super().__init__(responses, 11)
    

class HareRandom(Redistributor):
    """
    Choose ballots randomly, without repetition.
    """
    def __init__(self, responses):
        self.responses = responses.copy()

    def __next__(self):
        try:
            while True:
                try:
                    if len(self.responses):
                        n = random.randint(0, len(self.responses) - 1)
                        item = self.responses.pop(n)
                        yield item
                    else:
                        raise StopIteration()
                finally:
                    pass
        finally:
            pass
        return None

    __call__ = __next__
    __iter__ = __next__

        

class Gregory(Redistributor):
    """
    """
    pass

class Wright(Redistributor):
    """
    """
    pass

class Meek(Redistributor):
    """
    """
    pass

class Warren(Redistributor):
    """
    """
    pass


