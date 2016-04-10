import fnmatch

""" Simple filter class """
class Filter:
    def __init__(self):
        self.filters = []

    def parse(self, path):
        for line in open(path, 'r'):
            if line not in self.filters:
                self.filters.append(line)

    def check(self, name):
        for case in self.filters:
            if fnmatch.fnmatchcase(name, case):
                return True

        return False
