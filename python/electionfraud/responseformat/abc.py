# -*- python -*-

import abc

import electionfraud.responseformat.exception as rfx

class Abstract(metaclass=abc.ABCMeta):
    """
    The various response formats are derived from this abstract base class.
    """

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def validate(self, responses, field=None):
        """
        Checks that the response is in the right format (i.e. data type).
        May also do other checks at the response format's discretion.
        Must throw an exception if the response is not proper.
        Must return None if the response is proper.
        """
        raise NotImplemented()
    
    def validate_choices(self, responses, field=None):
        """
        Validate a particular choice against the field.  
        Must return None if the choices all validate.
        Must throw an exception if a choice is not valid.
        When field = None, write-in choices are permitted.
        This simpler version should work for iterable responses.
        field can be any type that supports 'in' or 'not in' comparison.
        """
        if field is None:
            return
        for choice in responses:
            if choice not in field:
                raise rfx.InvalidChoice()

    def detect_duplicates(self, responses):
        """
        Check the set of responses for duplicates, if necessary.
        Must return None if there are no duplicates.
        Must throw an exception if there are duplicates.
        This implementation compares the size of the original responses to 
        the size of a set()ed version.
        """
        if len(responses) > len(set(responses)):
            raise rfx.DuplicateChoice()
