import src

# It's not important that the file really exists.
FILES = ["test_1.png"]


def test_filter_in():
    f = src.Filter()
    f.add("*.png")

    assert f.check(FILES[0])


def test_filter_out():
    f = src.Filter()
    f.add("*.jpg")

    assert not f.check(FILES[0])


def test_filter_std_in():
    f = src.get_standard_filter()

    assert f.check(FILES[0])


def test_filter_parse_in():
    f = src.Filter()
    f.parse("./src/tests/files/filter.lst")

    assert f.check(FILES[0])


def test_filter_parse_out():
    f = src.Filter()
    f.parse("./src/tests/files/filter.lst")

    assert not f.check("test.nope")
