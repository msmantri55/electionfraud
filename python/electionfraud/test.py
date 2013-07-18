# -*- python -*-

import unittest

from electionfraud.responseformat import ChooseExactly, ChooseNoMoreThan, RankInOrderOfPreference, RankAllInOrderOfPreference, WrongNumberOfChoices

class ResponseFormatTest(unittest.TestCase):

    def setUp(self):
        self.field = set(['Chattanooga', 'Knoxville', 'Memphis', 'Nashville'])

class TestChooseExactly(ResponseFormatTest):

    def setUp(self):
        ResponseFormatTest.setUp(self)
        self.rf = ChooseExactly(2)
    
    def test_too_many(self):
        responses = set(['Chattanooga', 'Knoxville', 'Memphis'])
        self.assertRaises(WrongNumberOfChoices, self.rf.validate, responses, self.field)

    def test_too_few(self):
        responses = set(['Chattanooga'])
        self.assertRaises(WrongNumberOfChoices, self.rf.validate, responses, self.field)

    def test_none_at_all(self):
        self.assertRaises(WrongNumberOfChoices, self.rf.validate, set(), self.field)

class TestChooseNoMoreThan(ResponseFormatTest):
    
    def setUp(self):
        ResponseFormatTest.setUp(self)
        self.rf = ChooseNoMoreThan(2)

    def test_too_many(self):
        responses = set(['Chattanooga', 'Knoxville', 'Memphis'])
        self.assertRaises(WrongNumberOfChoices, self.rf.validate, responses, self.field)

class TestRiOoP(ResponseFormatTest):

    def setUp(self):
        ResponseFormatTest.setUp(self)
        self.rf = RankInOrderOfPreference()

class TestRAiOoP(ResponseFormatTest):

    def setUp(self):
        ResponseFormatTest.setUp(self)
        self.rf = RankAllInOrderOfPreference()

    def test_too_few(self):
        responses = ['Chattanooga', 'Knoxville', 'Memphis']
        self.assertRaises(WrongNumberOfChoices, self.rf.validate, responses, self.field)


if __name__ == '__main__':
    unittest.main()
