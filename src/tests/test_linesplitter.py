"""Tests the linesplitter module."""

import querycrafter.linespliter as linespliter


def test_split_line_1():
    """Tests the split_line function."""
    retrieved = linespliter.split_line("", 80)
    assert isinstance(retrieved, list)
    assert len(retrieved) == 1
    assert retrieved[0] == ""


def test_split_line_2():
    """Tests the split_line function."""
    line = "   junk    "
    retrieved = linespliter.split_line(line, 80)
    assert isinstance(retrieved, list)
    assert len(retrieved) == 1
    assert retrieved[0] == line.rstrip()


def test_split_line_3():
    """Tests the split_line function."""
    max_length = 80
    line = "0123456789" * 9
    retrieved = linespliter.split_line(line, max_length)
    assert isinstance(retrieved, list)
    assert len(retrieved) == 2
    assert len(retrieved[0]) <= max_length
    assert len(retrieved[1]) <= max_length


def test_split_line_4():
    """Tests the split_line function."""
    max_length = 80
    leading_spaces = "      "
    line = leading_spaces + "0123456789" * 9
    retrieved = linespliter.split_line(line, max_length)
    assert isinstance(retrieved, list)
    assert len(retrieved) == 2
    for line in retrieved:
        assert len(line) <= max_length
        assert line.startswith(leading_spaces)
