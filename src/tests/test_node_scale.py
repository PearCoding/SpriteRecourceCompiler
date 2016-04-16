import src


FILES = ["./src/tests/files/test_1.png", "./src/tests/files/test_2.png", "./src/tests/files/test_3.png"]


def test_node_scale_sqr():
    p = src.Parser()
    p.from_string(
        """
            <package>
            <input filter="*">
            <output>
                <scale factor="2" />
            </output>
            </input>
            </package>
        """)
    proc = src.Processor()
    p.parse(proc)

    outputs = proc.execute(FILES)

    assert len(outputs) == 3
    for output in outputs:
        assert output.width == 64
        assert output.height == 64


def test_node_scale():
    p = src.Parser()
    p.from_string(
        """
            <package>
            <input filter="*">
            <output>
                <scale factor="2,4" />
            </output>
            </input>
            </package>
        """)
    proc = src.Processor()
    p.parse(proc)

    outputs = proc.execute(FILES)

    assert len(outputs) == 3
    for output in outputs:
        assert output.width == 64
        assert output.height == 128
