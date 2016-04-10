from enum import Enum, unique


@unique
class PackMode(Enum):
    VarAnim = 0
    Tight = 1

    def __str__(self):
        return '{0}'.format(self.name)


@unique
class PaddingMode(Enum):
    Transparent = 0
    Fill = 1
    Black = 2
    White = 3
    Magenta = 4

    def __str__(self):
        return '{0}'.format(self.name)