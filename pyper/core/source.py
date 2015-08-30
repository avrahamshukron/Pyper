from io import FileIO
import os


class IndentedContext(object):
    """
    Context manager for indented code.
    """
    def __init__(self, source_file):
        self.source_file = source_file

    def __enter__(self):
        self.source_file.indent()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.source_file.dedent()


class SourceFile(object):

    WHITESPACE = " "
    FOUR_SPACES = WHITESPACE * 4
    TWO_SPACES = WHITESPACE * 2
    TAB = "\t"

    def __init__(self, stream, indentation=TAB, line_separator=os.linesep):
        """
        Initializes a new source file.

        :param stream: The underlying stream that the source code will be
            written to. Should be an object that has a ``write`` method.
        :param indentation: The indentation string of one indentation unit.
        :type indentation: str
        :param line_separator: The line separator for this file.
        :type line_separator: str
        """
        self._stream = stream
        self._indentation = indentation
        self._line_separator = line_separator
        self._indentation_level = 0
        self._is_new_line = True
        self._elements = []

    def indent(self, levels=1):
        """
        Increases the indentation by the given levels.

        :param levels: How many levels to indent.
        :return: self
        """
        self._indentation_level += levels
        return self

    def dedent(self, levels=1):
        """
        Decreases the indentation by the given levels.

        :param levels: How many levels to dedent.
        :return: self.
        """
        self._indentation_level = max(self._indentation_level - levels, 0)
        return self

    def indented_block(self):
        return IndentedContext(self)

    def add_element(self, code_element):
        """
        Adds a code element to the source file.

        :param code_element: The code element
        :type code_element: CodeElement
        :return: self
        """
        self._elements.append(code_element)
        return self

    def write(self, text, *args):
        """
        Writes a text at the current indentation level.

        :param text: The text to write.
        :param args: Any format argument for the text.
        :return: self.
        """
        if not text:
            return self

        if self._is_new_line:
            self._stream.write(self._indentation * self._indentation_level)
            self._is_new_line = False
        self._stream.write(text % args)
        return self

    def write_line(self, line):
        """
        Writes a text and insert a line feed at the end.

        :param line: The line to write.
        :return: self
        """
        return self.write(line).line_feed()

    def line_feed(self):
        """
        Inserts a line feed. Does not change the indentation level.

        :return: self.
        """
        self._stream.write(self._line_separator)
        self._is_new_line = True
        return self

    def emit(self):
        for element in self._elements:
            element.emit(self)

    def emit_element(self, element):
        if element is not None:
            element.emit(self)
        return self

    def emit_indented(self, element):
        if element is not None:
            with self.indented_block():
                self.emit_element(element)
        return self

    def is_new_line(self):
        return self._is_new_line
