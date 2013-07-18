# -*- python -*-

import uuid

from datetime import datetime
from electionfraud import ElectionException

class Election:

    """
    An election contains:
    * A list of questions to be decided by the voters.
    * A set of voters who are permitted to participate.
    * A ballot box which associates voters with cast ballots.
    * A collection of results, one for each question.
    * 
    """
    
    def __init__(self, deadline=None, polls=(None,None), absentee=(None,None)):
        self._id = uuid.uuid4()
        self.questions = []
        self.voters = set()
        self.ballotbox = {}
        self.results = {}
        self._registration_deadline = deadline
        self._polls_open, self.polls_closed = polls
        self._absentee_open, self.absentee_closed = absentee

    def register_voter(voter):
        """
        Attempt to register a voter for this election.
        Raises an exception if the registration deadline has passed.
        """
        if datetime.now() > self._registration_deadline:
            raise ElectionException('voter registration deadline has passed')
        self.voters = self.voters | voter
        self.ballotbox[voter] = None

    def vote_at_polling_place(self, voter, ballot):
        """
        Allows a voter to cast a ballot in person if the polls are open.
        Raises an exception otherwise.
        """
        if self._polls_open == self._polls_closed:
            raise ElectionException('in-person voting not accepted for this election')
        now = datetime.now()
        if now < self._polls_open:
            raise ElectionException('polls are not yet open')
        if now > self._polls_closed:
            raise ElectionException('polls have been closed')
        self._vote(voter, ballot)

    def vote_absentee(self, voter, ballot):
        """
        Allows a voter to cast an absentee ballot if within the appropriate
        time window.  Raises an exception otherwise.
        """
        if self._absentee_open == self._absentee_closed:
            raise ElectionException('absentee ballots not accepted for this election')
        now = datetime.now()
        if now < self._absentee_open:
            raise ElectionException('not accepting absentee ballots yet')
        if now > self._absentee_closed:
            raise ElectionException('absentee ballots no longer accepted')
        self._vote(voter, ballot)

    def _vote(self, voter, ballot):
        """
        Allows a voter to cast a ballot if they are registered and they
        have not previously voted in this election.  Raises an exception
        otherwise.
        """
        if voter not in self.voters:
            raise ElectionException('not a registered voter')
        try:
            _ = self.ballotbox[voter]
        except KeyError:
            self.ballotbox[voter] = (voter, ballot)
        else:
            raise ElectionException('that voter has already cast a ballot')

    def resolve(self):
        """
        Counts all the cast ballots, one question at a time.
        """
        for q in self.questions:
            self.results[q] = q.resolve(self.ballotbox))
