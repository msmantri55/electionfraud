# -*- python -*-

import unittest

import electionfraud.testdata as eftd

import electionfraud.responseformat.choose as choose
import electionfraud.responseformat.exception as rfx
import electionfraud.responseformat.pair as pair
import electionfraud.responseformat.rank as rank
import electionfraud.responseformat.rate as rate



class ResponseFormatTest(unittest.TestCase):

    def setUp(self):
        self.field = set(eftd.TENNESSEE.keys())

class TestChooseExactly(ResponseFormatTest):

    def setUp(self):
        ResponseFormatTest.setUp(self)
        self.rf = choose.ChooseExactly(2)
    
    def test_too_many(self):
        responses = set(list(eftd.TENNESSEE.keys())[0:3])
        self.assertRaises(rfx.WrongNumberOfChoices, self.rf.validate, responses, self.field)

    def test_too_few(self):
        responses = set([list(eftd.TENNESSEE.keys())[0]])
        self.assertRaises(rfx.WrongNumberOfChoices, self.rf.validate, responses, self.field)

    def test_none_at_all(self):
        self.assertRaises(rfx.WrongNumberOfChoices, self.rf.validate, set(), self.field)

class TestChooseNoMoreThan(ResponseFormatTest):
    
    def setUp(self):
        ResponseFormatTest.setUp(self)
        self.rf = choose.ChooseNoMoreThan(2)

    def test_too_many(self):
        responses = set(list(eftd.TENNESSEE.keys())[0:3])
        self.assertRaises(rfx.WrongNumberOfChoices, self.rf.validate, responses, self.field)

class TestRiOoP(ResponseFormatTest):

    def setUp(self):
        ResponseFormatTest.setUp(self)
        self.rf = rank.RankInOrderOfPreference()

    def test_format(self):
        responses = list(eftd.TENNESSEE.keys())
        self.assertIsNone(self.rf.validate(responses, self.field))

class TestRAiOoP(ResponseFormatTest):

    def setUp(self):
        ResponseFormatTest.setUp(self)
        self.rf = rank.RankAllInOrderOfPreference()

    def test_too_few(self):
        responses = list(eftd.TENNESSEE.keys())[0:3]
        self.assertRaises(rfx.WrongNumberOfChoices, self.rf.validate, responses, self.field)

class TestRNMTiOoP(ResponseFormatTest):

    def setUp(self):
        ResponseFormatTest.setUp(self)
        self.rf = rank.RankNoMoreThanInOrderOfPreference(3)

    def test_too_many(self):
        responses = list(eftd.TENNESSEE.keys())
        self.assertRaises(rfx.WrongNumberOfChoices, self.rf.validate, responses, self.field)

class TestRatings(ResponseFormatTest):
    
    def setUp(self):
        ResponseFormatTest.setUp(self)
        self.rf = rate.Ratings(5)

    def test_bad_ratings(self):
        responses = [(x, x) for x in self.field]
        self.assertRaises(rfx.NonIntegerRating, self.rf.validate, responses, self.field)

    def test_negative_ratings(self):
        responses = [(x,-1) for x in self.field]
        self.assertRaises(rfx.NegativeRating, self.rf.validate, responses, self.field)

    def test_overly_positive_ratings(self):
        responses = [(x, 5 + len(self.field)) for x in self.field]
        self.assertRaises(rfx.OverMaximumRating, self.rf.validate, responses, self.field)

class TestBudget(ResponseFormatTest):
    
    def setUp(self):
        ResponseFormatTest.setUp(self)
        self.rf = rate.Budget(20)

    def test_excess(self):
        responses = [(x, 19 + len(self.field)) for x in self.field]
        self.assertRaises(rfx.OverBudget, self.rf.validate, responses, self.field)

class TestPairwise(ResponseFormatTest):

    def setUp(self):
        ResponseFormatTest.setUp(self)
        self.rf = pair.Pairwise()

    def test_non_tuple(self):
        self.assertRaises(TypeError, self.rf.validate, self.field, self.field)

    def test_mirror(self):
        responses = [(x, x) for x in self.field]
        self.assertRaises(rfx.SelfPair, self.rf.validate, responses, self.field)

    def test_duplicates_forward(self):
        responses = [tuple(list(eftd.TENNESSEE.keys())[0:2])] * 2
        self.assertRaises(rfx.DuplicateChoice, self.rf.validate, responses, self.field)

    def test_duplicates_backward(self):
        response = tuple(list(eftd.TENNESSEE.keys())[0:2])
        x, y = response
        esnopser = (y, x)
        responses = [response, esnopser]
        self.assertRaises(rfx.MakeUpYourMind, self.rf.validate, responses, self.field)     

class TestAllPossiblePairwise(ResponseFormatTest):

    def setUp(self):
        ResponseFormatTest.setUp(self)
        self.rf = pair.AllPossiblePairwise()

    def test_wrong_number(self):
        responses = []

    def test_right_number(self):
        responses = []
        choices = list(eftd.TENNESSEE.keys())
        deleted = []
        while len(choices) > 0:
            pairs = [ (choices[0], other) for other in self.field - set(deleted) - set(choices[0:1]) ]
            responses.extend(pairs)
            deleted.append(choices.pop(0))
        self.assertIsNone(self.rf.validate(responses, self.field))

if __name__ == '__main__':
    unittest.main()
