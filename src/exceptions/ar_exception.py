
class ARException(BaseException):

    def __init__(self, exit_code, msg, **details):
        self.exit = exit_code
        self.msg = msg
        self._details = details

    def __str__(self):
        return self.msg

    def __int__(self):
        return self.exit

    @property
    def details(self):
        return self._details

    @property
    def dump(self):
        return ','.join([self.msg, self.exit, self._details])

