# -*- python -*-

import logging
import unittest

import electionfraud.testdata as eftd
import electionfraud.redist as redist

logging.basicConfig(level=logging.DEBUG)

class RedistributorTest(unittest.TestCase):
    pass

class TestIdentity(RedistributorTest):

    def setUp(self):
        self.rd = redist.Identity(eftd.FOOD_STV_20)

    def test_identity(self):
        redistributed = [x for x in self.rd]
        self.assertEqual(redistributed, eftd.FOOD_STV_20)

class TestNthSubset(RedistributorTest):
    
    def setUp(self):
        self.n = 7

    def test_divisor(self):
        self.assertRaises(ValueError, redist.NthSubset, eftd.FOOD_STV_20, 1)
        self.assertRaises(ValueError, redist.NthSubset, eftd.FOOD_STV_20, 2)
        self.assertRaises(ValueError, redist.NthSubset, eftd.FOOD_STV_20, 4)

    def test_depth(self):
        rd = redist.NthSubset(range(20), self.n);
        redistributed = [x for x in rd]
        self.assertEqual(redistributed, [6, 13, 0, 7, 14, 1, 8, 15, 2, 9, 16, 3, 10, 17, 4, 11, 18, 5, 12, 19])

    def test_food_distribution(self):
        rd = redist.NthSubset(eftd.FOOD_STV_20, self.n)
        redistributed = [x for x in rd]
        self.assertEqual(len(eftd.FOOD_STV_20), len(redistributed))
        self.assertNotEqual(eftd.FOOD_STV_20, redistributed)

        

if __name__ == '__main__':
    unittest.main()

