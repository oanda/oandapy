"""Exceptions."""

class BadEnvironment(Exception):
    """environment should be: sandbox, practice or live."""
    def __init__(self, msg):
        super(BadEnvironment, self).__init__(msg)
