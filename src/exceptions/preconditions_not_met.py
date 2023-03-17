from .ar_exception import ARException


class ARPreconditionsException(ARException):

    def __init__(self, exit_code, msg, **details):
        self.exit = exit_code or 30
        self.msg = msg or 'Preconditions not met!'
        self._details = details


