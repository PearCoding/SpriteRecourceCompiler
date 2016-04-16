import src


FILES = ["./src/tests/files/test_1.png", "./src/tests/files/test_2.png", "./src/tests/files/test_3.png"]


def test_node_resize_sqr():
    p = src.Parser()
    p.from_string(
        """
            <package>
            <input filter="*">
            <output>
                <resize size="16" />
            </output>
            </input>
            </package>
        """)
    proc = src.Processor()
    p.parse(proc)

    outputs = proc.execute(FILES)

    assert len(outputs) == 3
    for output in outputs:
        assert output.width == 16
        assert output.height == 16


def test_node_resize():
    p = src.Parser()
    p.from_string(
        """
            <package>
            <input filter="*">
            <output>
                <resize size="16,64" />
            </output>
            </input>
            </package>
        """)
    proc = src.Processor()
    p.parse(proc)

    outputs = proc.execute(FILES)

    assert len(outputs) == 3
    for output in outputs:
        assert output.width == 16
        assert output.height == 64
