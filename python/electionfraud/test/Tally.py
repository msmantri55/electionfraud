#!/usr/bin/env python3

import unittest
import Tally

class TestTally(unittest.TestCase):

    def test_tally(self):
        t = Tally.Tally()
        votes = [x for x in 'asdaghsdlfhalglkajsdfkljghasklgfaklsjalsajsaskaj']
        t.tally(votes)
        expected = []
        for x in 'asdfghjkl':
            expected.append((x, len([v for v in votes if x == v])))
        for y in expected:
            v, _ = y
            self.assertEqual(t.results[v], y)

unittest.main()
