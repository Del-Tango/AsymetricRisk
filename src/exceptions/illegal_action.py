from .ar_exception import ARException


class ARIllegalActionException(ARException):

    def __init__(self, exit_code, msg, **details):
        self.exit = exit_code or 20
        self.msg = msg or 'Illegal action!'
        self._details = details


