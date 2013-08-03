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

class TestCincinnati(RedistributorTest):

    def test_cincy_divisor(self):
        self.assertRaises(ValueError, redist.Cincinnati, range(11))
    
    def test_cincy_depth(self):
        rd = redist.Cincinnati(range(20))
        redistributed = [x for x in rd]
        self.assertEqual(redistributed, [10, 1, 12, 3, 14, 5, 16, 7, 18, 9, 0, 11, 2, 13, 4, 15, 6, 17, 8, 19])

    def test_cincy_food(self):
        rd = redist.Cincinnati(eftd.FOOD_STV_20)
        redistributed = [x for x in rd]
        self.assertEqual(len(eftd.FOOD_STV_20), len(redistributed))
        self.assertNotEqual(eftd.FOOD_STV_20, redistributed)
        
class TestHareRandom(RedistributorTest):

    def setUp(self):
        pass

    def test_hare_depth(self):
        tedium = 10
        shuffles = list()
        for i in range(tedium):
            rd = redist.HareRandom(eftd.FOOD_STV_20)
            shuffle = [x for x in rd]
            self.assertEqual(len(eftd.FOOD_STV_20), len(shuffle))
            self.assertNotEqual(eftd.FOOD_STV_20, shuffle)
            shuffles.append(shuffle)
        for i in range(tedium - 1):
            self.assertNotEqual(shuffles[i], shuffles[i + 1])
        


if __name__ == '__main__':
    unittest.main()

