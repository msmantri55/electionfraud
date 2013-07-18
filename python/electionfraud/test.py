# -*- python -*-

import unittest

from electionfraud.responseformat import ChooseExactly, WrongNumberOfChoices

class ResponseFormatTest(unittest.TestCase):

    def setUp(self):
        self.field = set(['Chattanooga', 'Knoxville', 'Memphis', 'Nashville'])

class TestChooseExactly(ResponseFormatTest):
    
    def test_validate(self):
        rf = ChooseExactly(2)
        responses = set(['Chattanooga', 'Knoxville', 'Memphis'])
        self.assertRaises(WrongNumberOfChoices, rf.validate, responses, self.field)
        responses = set(['Chattanooga'])
        self.assertRaises(WrongNumberOfChoices, rf.validate, responses, self.field)
        self.assertRaises(WrongNumberOfChoices, rf.validate, set(), self.field)


if __name__ == '__main__':
    unittest.main()
