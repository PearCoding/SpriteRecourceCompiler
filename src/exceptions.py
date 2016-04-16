class SRCException(Exception):
    pass


class XMLError(SRCException):
    def __init__(self, str):
        self.str = str

    def __str__(self):
        return 'XML Error: {0}'.format(self.str)


class ProcessorError(SRCException):
    def __init__(self, str):
        self.str = str

    def __str__(self):
        return 'Processing Error: {0}'.format(self.str)
