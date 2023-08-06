# Custom exception class FauditException

class FauditException(Exception):
    """Base class for all other exceptions"""
    def __init__(self, *args: object):
        super().__init__(*args)
        self.error=args[0]  