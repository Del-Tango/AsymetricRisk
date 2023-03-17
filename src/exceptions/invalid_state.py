from .ar_exception import ARException


class ARInvalidStateException(ARException):

    def __init__(self, exit_code, msg, **details):
        self.exit = exit_code or 10
        self.msg = msg or 'Invalid state!'
        self._details = details


