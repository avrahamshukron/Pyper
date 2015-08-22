
class CodeElement(object):
    """
    Base class for any code element
    """

    def emit(self, source_file):
        """
        Emits the current code element into the supplied source file.

        :param source_file:
        :type source_file: SourceFile.
        """
        raise NotImplementedError("%s is an Abstract class." %
                                  (self.__class__.__name__,))
