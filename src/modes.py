from enum import Enum, unique


@unique
class PackMode(Enum):
    VarAnim = 0  # FIXME: Not implemented!
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


# TODO: Add more standard stuff
@unique
class ImageFilterMode(Enum):
    Normal = 0
    Multiply = 1
    Add = 2
    Sub = 3

    def __str__(self):
        return '{0}'.format(self.name)


@unique
class InputTypeMode(Enum):
    File = 0
    Output = 1
    Input = 2
    Package = 3

    def __str__(self):
        return '{0}'.format(self.name)
