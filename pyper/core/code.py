from StringIO import StringIO


class CodeElement(object):
    """
    Base class for any code element
    """

    def emit(self, source_file):
        """
        Emits the current code element into the supplied source file.

        :param source_file:
        :type source_file: pyper.core.source.SourceFile
        """
        raise NotImplementedError("%s is an Abstract class." %
                                  (self.__class__.__name__,))


class TextCodeElement(CodeElement):
    """
    A basic code element for free text.
    Used mainly for lazy testing stuff, and generally discouraged as an actual
    code element.
    """
    def __init__(self, text):
        self.text = StringIO(text)

    def add_line(self, line):
        self.text.write("\n" + line)

    def emit(self, source_file):
        source_file.write(self.text.getvalue())
        self.text.close()