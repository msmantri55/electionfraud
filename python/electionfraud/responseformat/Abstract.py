# -*- python -*-

from electionfraud import ElectionException

class Abstract:

    """
    The various response formats are derived from this abstract base class.
    """

    def __init__(self):
        pass

    def validate(self, responses, field=None):
        """
        Checks that the response is in the right format (i.e. data type)
        and that the choices in it are limited to the field of possible
        choices.  When field = None, write-in choices are permitted.
        If the data types match up properly, should then go on to 
        invoke:
        validate_choices
        detect_duplicates
        """
        raise ElectionException('responseformat not properly subclassed')
    
    def validate_choices(self, responses, field=None):

        """
        Validate a particular choice against the field.  When field = None,
        write-in choices are permitted.
        field can be any type that supports 'in' or 'not in' comparison.
        """

        if field == None:
            return
        for choice in responses:
            if choice not in field:
                raise InvalidChoiceException(choice, field)

    def detect_duplicates(self, responses):
        """
        Should work for the simpler derived classes.  Compares the size
        of the original responses to a mashed-into-set version.
        """
        if len(responses) > len(set(responses)):
            raise ResponseException('duplicate choices not allowed')
