import src
import pytest


def get_tile():
    return src.Tile("./src/tests/test.png")


def test_nofile():
    with pytest.raises(IOError):
        tile = src.Tile("nope")


def test_pos():
    tile = get_tile()
    assert tile.x == -1
    assert tile.y == -1


def test_size():
    tile = get_tile()
    assert tile.width == 32
    assert tile.height == 32


def test_area():
    tile = get_tile()
    assert tile.area() == 32*32
