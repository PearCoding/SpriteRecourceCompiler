from enum import Enum, unique


@unique
class PackMode(Enum):
    VarAnim = 0
    Tight = 1


@unique
class PaddingMode(Enum):
    Transparent = 0
    Fill = 1
    Black = 2