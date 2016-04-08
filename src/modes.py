from enum import Enum, unique


@unique
class PackMode(Enum):
    VarAnim = 0
    Tight = 1