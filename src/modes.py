from enum import Enum, unique


@unique
class PackMode(Enum):
    VarAnim = 0
    VarAnimTight = 1
    Tight = 2