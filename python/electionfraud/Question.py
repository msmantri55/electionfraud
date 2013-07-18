# -*- python -*-

import uuid

class Question:

    """
    A question contains:
    * some text describing the question to be decided by the voters
    * a set of choices
    * the order in which the choices are presented to the voter
    * the expected format of responses
    * the method by which responses will be counted
    * a method for dealing with spoiled ballots
    """

    def __init__(self, choices=set(), arrangement=None, responseformat=None, countmethod=None, spoilmethod=None):
        self._id = uuid.uuid4()
        self.text = None
        self.choices = choices
        self.arrangement = arrangement
        self.responseformat = responseformat
        self.countmethod = countmethod
        self.spoilmethod = spoilmethod
        self.spoiled = []
        self.results = None

    def resolve(self, ballotbox):
        """
        Checks each ballot in the ballot box to see if it is spoiled, i.e.
        the terms of the response format were violated.  Valid ballots are 
        then counted according to the selected counting method.  Ballots are
        spoiled on a question-by-question basis, not in their entirety.
        """
        self.countmethod.reset()
        for voter in ballotbox.keys():
            _, ballot = ballotbox[voter]
            response = ballot[self]
            try:
                self.responseformat.validate(response)
            except ElectionException as e:
                self.spoil(response, e)
            else:
                self.countmethod.count(response)
        self.results = self.countmethod.results()

    def spoil(self, response, reason):
        self.spoiled.append((response, reason))
