"""Exceptions."""

class BadEnvironment(Exception):
    """environment should be: sandbox, practice or live."""
    def __init__(self, environment):
        msg = "Environment '%s' does not exist" % environment
        super(BadEnvironment, self).__init__(msg)
