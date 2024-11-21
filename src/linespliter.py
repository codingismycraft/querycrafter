"""Defines a class to split long lines to formated sections."""

import collections


def split_line(line, max_length):
    """Splits the passed in line to substrings.

    Used to format strings in a doc string and fit them properly.

    :param str line: The line of text to be formatted.
    :param int max_length: The maximum allowed length of the formatted line.

    :returns: The list of the wrapped lines.
    :rtype: list[str]
    """
    splitter = _LineSplitter(line, max_length)
    return splitter.get_split()


_HeadAndTail = collections.namedtuple("_HeadAndTail", ["head", "tail"])


class _LineSplitter:
    """Used to split a long string to list of substrings.

    :ivar int _max_length: The maximum allowed length of each substring.
    :ivar str _line: The line to split.
    :ivar str _leading_spaces: Consists of the leading spaces.

    :icvar int _DEFAULT_MAX_LENGTH: The default max length to use.
    """

    _DEFAULT_MAX_LENGTH = 80

    _max_length = None
    _line = None
    _leading_spaces = None

    def __init__(self, line, max_length=None):
        """Initializer.

        :param str line: The line to split.

        :param int max_length: The max length of the string; if None
        then tne _DEFAULT_MAX_LENGTH will be used.
        """
        self._line = line.rstrip()
        self._max_length = max_length or self._DEFAULT_MAX_LENGTH
        self._leading_spaces = self._get_leading_spaces(self._line)

    def get_split(self):
        """Splits the line based in the max length.

        :returns: A list of strings.
        :rtype: list [str]
        """
        if len(self._line) <= self._max_length:
            return [self._line]

        lines = []
        head, tail = self._get_head_and_tail(self._line)
        while head:
            lines.append(head)
            head, tail = self._get_head_and_tail(tail)

        lines_with_leading_spaces = [
            self._leading_spaces + line for line in lines
        ]
        return lines_with_leading_spaces

    def _get_head_and_tail(self, line):
        """Returns the first and remainder substrings for the passed in line.

        :param str line: The line to split.

        :returns: A _HeadAndTail tuple consisting of head and tail.
        :rtype: tuple
        """
        line = line.strip()
        if len(line) <= self._max_length:
            return _HeadAndTail(line, "")

        cutoff = self._max_length - 1 - len(self._leading_spaces)
        index = self._max_length - 1 - len(self._leading_spaces)
        while index >= 0:
            if line[index] == ' ':
                cutoff = index
                break
            index -= 1
        return _HeadAndTail(line[:cutoff], line[cutoff:])

    @classmethod
    def _get_leading_spaces(cls, line):
        """Returns the leading spaces as a string.

        :returns: The leading spaces as a string.
        :rtype: str
        """
        leading_spaces = ''
        for c in line:
            if c == ' ':
                leading_spaces += ' '
            else:
                break
        return leading_spaces
