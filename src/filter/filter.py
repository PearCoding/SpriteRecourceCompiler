import fnmatch


class Filter:
    """ Simple filter class """
    def __init__(self):
        self.filters = []

    def parse(self, path):
        for line in open(path, 'r'):
            self.add(line.strip())

    def add(self, case):
        if case not in self.filters:
            self.filters.append(case)

    def check(self, name):
        for case in self.filters:
            if fnmatch.fnmatchcase(name, case):
                return True

        return False
