# -*- python -*-

import uuid

class Voter:

    """
    A voter, intentionally devoid of any real identifying information
    save a UUID.
    """

    def __init__(self):
        self._id = uuid.uuid4()

    def __str__(self):
        return self._id

